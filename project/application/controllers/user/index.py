from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
import bcrypt

from application.models.user import User
from application.database.index import db
from application.errors import FieldsNotValidError
from application.controllers.utils import get_redirect_error, flatten_from_errors
from application.controllers.user.form import SigninForm, SignupForm

@app.route("/signup", methods=['GET'])
def render_signup():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  return render_template('users/signup.html', errors=errors)

@app.route("/signup", methods=['POST'])
def signup():
  app.logger.info('Request Received')

  form = SignupForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  if len(errors) == 0:
    app.logger.info('Searcing for user')

    username = form.username.data
    password = form.password.data
    name = form.name.data

    db.session.begin()
    existing_user = db.session.query(User).filter(User.username == username).first()
    if existing_user == None:
      try:
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        new_user = User(username=username, name=name, password=hashed, active=True)
        db.session.add(new_user)
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('adding user')
    else:
      errors.append(FieldsNotValidError("Account with email already exists"))

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    return render_template('users/signup.html', errors=errors)

  app.logger.info('everything was OK')
  return redirect(url_for('render_signin'))

@app.route("/login", methods=['GET'])
def render_signin():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  return render_template('users/login.html', errors=errors)

@app.route("/login", methods=['POST'])
def login():
  app.logger.info('Request Received')

  form = SigninForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  if len(errors) == 0:
    app.logger.info('Searcing for user')

    username = form.username.data
    password = form.password.data

    user = db.session.query(User).filter(User.username == username).first()
    if user != None:
      try:
        if bcrypt.checkpw(password.encode('utf8'), user.password):
          print("USER LOGGED IN")
          app.logger.info('logging in')
          session['username'] = username
          session['user_id'] = user.user_id
        else:
          errors.append(FieldsNotValidError("Email/Password not valid"))
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        errors.append(e)
    else:
      errors.append(FieldsNotValidError("Email/Password not valid"))

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    return render_template('users/login.html', errors=errors)

  app.logger.info('everything was OK')
  return redirect(url_for('index'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  session.pop('username', None)
  session.pop('user_id', None)
  return redirect(url_for('login'))
