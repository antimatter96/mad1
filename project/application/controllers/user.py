from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from email_validator import validate_email, EmailNotValidError
import bcrypt

from application.models.user import User
from application.database.index import db
from application.errors import FieldsNotValidError
from application.controllers.utils import get_redirect_error

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
  name = request.form.get('name', "").strip()
  username = request.form.get('email', "").strip()
  password = request.form.get('password', "").strip()

  errors = []

  if len(name) == 0:
    errors.append(FieldsNotValidError("Name is required"))
  if len(username) == 0:
    errors.append(FieldsNotValidError("User name is required"))
  if len(password) == 0:
    errors.append(FieldsNotValidError("Password is requried"))
  elif len(password) < 8:
    errors.append(FieldsNotValidError("Minimum password length is 8"))

  try:
    username = validate_email(username).email
  except Exception as e:
    errors.append(FieldsNotValidError("User name " + str(e)))

  if len(errors) == 0:
    app.logger.info('Searcing for user')
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
  username = request.form.get('email', "").strip()
  password = request.form.get('password', "").strip()

  errors = []

  if len(username) == 0:
    errors.append(FieldsNotValidError("Username is required"))
  if len(password) == 0:
    errors.append(FieldsNotValidError("Password is requried"))
  elif len(password) < 8:
    errors.append(FieldsNotValidError("Minimum password length is 8"))

  try:
    username = validate_email(username).email
  except Exception as e:
    errors.append(FieldsNotValidError(str(e)))

  if len(errors) == 0:
    app.logger.info('Searcing for user')
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
