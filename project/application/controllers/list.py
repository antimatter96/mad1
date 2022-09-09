from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from application.models.card import Card
from application.models.list import List
from application.models.user import User

from application.database.index import db

from application.controllers.utils import get_redirect_error, create_redirect_error
from application.controllers.decorators import ensure_logged_in, ensure_list_exists
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
@app.route("/lists/new", methods=['POST'])
@ensure_logged_in
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
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('adding list')
    else:
      errors.append(FieldsNotValidError("Better to limit lists to 5"))

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    return render_template('lists/new_list.html', errors=errors)

  app.logger.info('everything was OK')
  return redirect(url_for('index'))

@app.route("/lists/new", methods=['GET'])
@ensure_logged_in
def render_create_list():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  return render_template('lists/new_list.html', errors=errors)

### Individual Lists

@app.route("/list/<list_id>/edit", methods=['GET'])
@ensure_logged_in
@ensure_list_exists
def render_edit_list(list_obj):
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  lists = db.session.query(List).all()
  return render_template('lists/edit_list.html', errors=errors, list_obj=list_obj, lists=lists, disable_list=True)

@app.route("/list/<list_id>/edit", methods=['POST'])
@ensure_logged_in
@ensure_list_exists
def edit_list(list_obj):
  name = request.form.get('name', "").strip()
  description = request.form.get('description', "").strip()

  errors = []
  if len(name) == 0:
    errors.append(FieldsNotValidError("Name is required"))
  if len(description) == 0:
    errors.append(FieldsNotValidError("Description is required"))

  if len(errors) == 0:
    try:
      list_obj.name = name
      list_obj.description = description
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      app.logger.error(e)
      db.session.rollback()
      errors.append(e)
    else:
      app.logger.info('list added list')

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    return render_template('lists/edit_list.html', errors=errors, list_obj=list_obj)

  app.logger.info('everything was OK')
  return redirect(url_for('render_list', list_id=list_obj.list_id))

@app.route("/lists/<list_id>/delete", methods=['POST'])
@ensure_logged_in
@ensure_list_exists
def delete_list(list_obj):
  mode = request.form.get('mode', "").strip()
  new_list_id = request.form.get('list_id', "").strip()

  errors = []

  if len(mode) == 0:
    errors.append(FieldsNotValidError("Mode is requried"))
  if mode != "move" and mode != "delete":
    errors.append(FieldsNotValidError("Mode should be move / delete"))

  if mode == "move":
    if len(new_list_id) == 0:
      errors.append(FieldsNotValidError("List is requried"))

    if len(new_list_id) > 0:
      try:
        new_list_id = int(new_list_id)
      except:
        errors.append(FieldsNotValidError("List is requried"))

    if len(errors) == 0:
      new_list_obj = db.session.query(List).filter(List.list_id == new_list_id).first()

      if new_list_obj == None:
        encoded_redirect_error = create_redirect_error("List with id " + str(new_list_id) + " does not exist")
        return redirect(url_for('render_create_list', redirect_error=encoded_redirect_error))

  if len(errors) == 0:
    if mode == "delete":
      try:
        for card in list_obj.cards:
          db.session.delete(card)
        db.session.delete(list_obj)
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('list deleted')
    else:
      try:
        card_ids = [card.card_id for card in list_obj.cards]
        db.session.delete(list_obj)
        db.session.flush()
        db.session.query(Card).filter(Card.card_id.in_(card_ids)).update({"parent_id": new_list_id})
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('list deleted')

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    encoded_redirect_error = create_redirect_error("\n".join(errors))
    return redirect(url_for('render_edit_list', list_id=list_obj.list_id, redirect_error=encoded_redirect_error))

  return redirect(url_for('index'))

@app.route("/list/<list_id>", methods=['GET'])
@ensure_logged_in
@ensure_list_exists
def render_list(list_obj):
  lists = db.session.query(List).all()
  return render_template('lists/list.html', errors=[], list_obj=list_obj, lists=lists)
