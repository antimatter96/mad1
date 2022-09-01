from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from application.models.card import Card
from application.models.list import List
from application.models.user import User

from application.database.index import db

from application.controllers.utils import ensure_logged_in, get_redirect_error, create_redirect_error
from application.errors import FieldsNotValidError

# Board
@app.route("/", methods=['GET'])
@ensure_logged_in
def index():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)
  
  current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
  lists = db.session.query(List).all()
  return render_template('board/index.html', errors=errors, lists=lists)

# Lists
@app.route("/list/new", methods=['POST'])
def create_list():
  app.logger.info('Request Received')

  name = request.form.get('name', "").strip()
  description = request.form.get('description', "").strip()

  errors = []

  if len(name) == 0:
    errors.append(FieldsNotValidError("Name is required"))
  if len(description) == 0:
    errors.append(FieldsNotValidError("Description is required"))

  if len(errors) == 0:
    db.session.begin()
    total_lists = db.session.query(List).all()
    if len(total_lists) < 5:
      try:
        current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
        new_list = List(name=name, description=description, creator=current_user)
        db.session.add(new_list)
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('adding list')
        db.session.commit()
    else:
      errors.append(FieldsNotValidError("Better to limit lists to 5"))

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    return render_template('lists/new_list.html', errors=errors)

  app.logger.info('everything was OK')
  return redirect(url_for('index'))

@app.route("/list/new", methods=['GET'])
@ensure_logged_in
def render_create_list():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  return render_template('lists/new_list.html', errors=errors)

@app.route("/list/edit/<list_id>", methods=['GET'])
@ensure_logged_in
def render_edit__list(list_id):
  list_obj = db.session.query(List).filter(List.list_id == list_id).first()
  if list_obj == None:
    encoded_redirect_error = create_redirect_error("List with id " + list_id + " does not exist")
    return redirect(url_for('render_create_list', redirect_error=encoded_redirect_error))

  return render_template('lists/edit_list.html', errors=[], list_obj=list_obj)

@app.route("/list/<list_id>", methods=['PUT'])
def edit_list(list_id):
  return "_list_students"

@app.route("/list/<list_id>", methods=['DELETE'])
def delete_list(list_id):
  return "_list_students"
