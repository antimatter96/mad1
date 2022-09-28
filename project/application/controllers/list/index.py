from flask import current_app as app
from flask import render_template, redirect, url_for, session

from application.models.card import Card
from application.models.list import List
from application.models.user import User

from application.database.index import db
from application.errors import FieldsNotValidError
from application.controllers.utils import get_redirect_error, create_redirect_error, flatten_from_errors, plot_timeline
from application.controllers.decorators import ensure_logged_in, ensure_list_exists
from application.controllers.list.form import DeleteListForm, ListForm

# Board
@app.route("/", methods=['GET'])
@ensure_logged_in
def index():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  lists = db.session.query(List).all()
  return render_template('board/index.html', errors=errors, lists=lists)

# Lists
@app.route("/lists/new", methods=['POST'])
@ensure_logged_in
def create_list():
  app.logger.info('Request Received')

  form = ListForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  if len(errors) == 0:
    name = form.name.data
    description = form.description.data

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
  form = ListForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  if len(errors) == 0:
    name = form.name.data
    description = form.description.data
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
  form = DeleteListForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  mode = form.mode.data
  new_list_id = form.list_id.data

  if len(errors) == 0 and mode == "move":
    new_list_obj = db.session.query(List).filter(List.list_id == new_list_id).first()

    if new_list_obj == None:
      encoded_redirect_error = create_redirect_error("List with id " + str(new_list_id) + " does not exist")
      return redirect(url_for('render_create_list', redirect_error=encoded_redirect_error))

    if new_list_obj.list_id == list_obj.list_id:
      encoded_redirect_error = create_redirect_error("List to move cards to cannot be same as list to delete")
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
  img_hash = plot_timeline(list_obj.timeline(), size=(10, 4), rotation=0)
  return render_template('lists/list.html', errors=[], list_obj=list_obj, lists=lists, img_hash=img_hash)
