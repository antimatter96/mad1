from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from application.models.card import Card
from application.models.list import List
from application.models.user import User

from application.database.index import db

from application.controllers.utils import ensure_logged_in
from application.errors import FieldsNotValidError

# Board
@app.route("/", methods=['GET'])
@ensure_logged_in
def index():
  current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
  lists = db.session.query(List).all()
  for li in lists:
    print(li.cards)
  return render_template('board/index.html', errors=[], lists=lists)
  # if login ->
  # else -> render_board()

# Lists
@app.route("/list", methods=['POST'])
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
    if len(total_lists) < 6:
      try:
        new_list = List(name=name, description=description)
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
    return render_template('board/new_list.html', errors=errors)

  app.logger.info('everything was OK')
  return redirect(url_for('index'))

@app.route("/list", methods=['GET'])
def render_create_list():
  return render_template('board/new_list.html', errors=[])

@app.route("/list/<list_id>", methods=['DELETE'])
def delete_list(list_id):
  return "_list_students"

@app.route("/list/<list_id>", methods=['PUT'])
def edit_list():
  return "_list_students"
