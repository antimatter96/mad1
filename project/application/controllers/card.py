from datetime import datetime

from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from application.models.card import Card
from application.models.list import List

from application.database.index import db
from application.errors import FieldsNotValidError, ResourceNotFound
from application.models.user import User
from application.controllers.utils import get_redirect_error, create_redirect_error
from application.controllers.decorators import ensure_card_exists, ensure_logged_in

@app.route("/cards/new", methods=['GET'])
@ensure_logged_in
def render_create_card():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  lists = db.session.query(List).with_entities(List.list_id, List.name).all()
  list_id = int(request.args.get('list_id', -1))
  disable_list = list_id in [l['list_id'] for l in lists]

  return render_template('cards/new_card.html', errors=errors, lists=lists, list_id=list_id, disable_list=disable_list)

@app.route("/cards/new", methods=['POST'])
@ensure_logged_in
def create_card():
  print(request.form)
  title = request.form.get('title', "").strip()
  content = request.form.get('content', "").strip()
  deadline = request.form.get('deadline', "").strip()
  list_id = request.form.get('list_id', "").strip()
  complete = request.form.get('complete', "").strip()

  errors = []

  if len(title) == 0:
    errors.append(FieldsNotValidError("Title is required"))
  if len(content) == 0:
    errors.append(FieldsNotValidError("Summary is required"))
  if len(deadline) == 0:
    errors.append(FieldsNotValidError("Deadline is requried"))
  if len(list_id) == 0:
    errors.append(FieldsNotValidError("List is requried"))

  if len(list_id) > 0:
    try:
      list_id = int(list_id)
    except:
      errors.append(FieldsNotValidError("List is requried"))
  if len(deadline) > 0:
    try:
      deadline = datetime.strptime(deadline, "%Y-%m-%d")
    except Exception as e:
      errors.append(FieldsNotValidError("Deadline is requried"))

  complete = complete == 'on'

  new_card = None
  if len(errors) == 0:
    app.logger.info('Searcing for user')
    current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    current_list = db.session.query(List).filter(List.list_id == list_id).first()
    if current_list != None:
      try:
        new_card = Card(title=title, content=content, deadline=deadline, complete=complete, creator=current_user, list=current_list)
        db.session.add(new_card)
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('card added')
    else:
      errors.append(FieldsNotValidError("List not found"))

  if len(errors) > 0:
    lists = db.session.query(List).with_entities(List.list_id, List.name).all()
    disable_list = list_id in [l['list_id'] for l in lists]
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    return render_template('cards/new_card.html', errors=errors, lists=lists, list_id=list_id, disable_list=disable_list)

  return redirect(url_for('list_card', card_id=new_card.card_id))

@app.route("/card/<card_id>", methods=['DELETE'])
@ensure_logged_in
def delete_card(card_id):
  return '_list_students'

@app.route("/card/<card_id>", methods=['GET'])
@ensure_logged_in
def list_card(card_id):
  return '_list_students'

@app.route("/card/<card_id>/edit", methods=['GET'])
@ensure_logged_in
@ensure_card_exists
def render_edit_card(card):
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  lists = db.session.query(List).with_entities(List.list_id, List.name).all()
  list_id = int(request.args.get('list_id', -1))
  disable_list = list_id in [l['list_id'] for l in lists]

  return render_template('cards/edit_card.html', errors=errors, lists=lists, list_id=list_id, disable_list=disable_list)

@app.route("/card/<card_id>/edit", methods=['POST'])
@ensure_logged_in
@ensure_card_exists
def edit_card(card):
  title = request.form.get('title', "").strip()
  content = request.form.get('content', "").strip()
  deadline = request.form.get('deadline', "").strip()
  list_id = request.form.get('list_id', "").strip()
  complete = request.form.get('complete', "").strip()

  errors = []

  if len(title) == 0:
    errors.append(FieldsNotValidError("Title is required"))
  if len(content) == 0:
    errors.append(FieldsNotValidError("Summary is required"))
  if len(deadline) == 0:
    errors.append(FieldsNotValidError("Deadline is requried"))
  if len(list_id) == 0:
    errors.append(FieldsNotValidError("List is requried"))

  if len(list_id) > 0:
    try:
      list_id = int(list_id)
    except:
      errors.append(FieldsNotValidError("List is requried"))
  if len(deadline) > 0:
    try:
      deadline = datetime.strptime(deadline, "%Y-%m-%d")
    except Exception as e:
      errors.append(FieldsNotValidError("Deadline is requried"))

  complete = complete == 'on'

  if len(errors) == 0:
    app.logger.info('Searcing for user')
    current_list = db.session.query(List).filter(List.list_id == list_id).first()
    if current_list != None:
      try:
        card.title = title
        card.content = content
        card.deadline = deadline
        card.complete = complete
        card.list = current_list
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
        errors.append(e)
      else:
        app.logger.info('card added')
    else:
      errors.append(FieldsNotValidError("List not found"))

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    encoded_redirect_error = create_redirect_error("\n".join(errors))
    return redirect(url_for('render_card_list', card_id=card_id, redirect_error=encoded_redirect_error))

  return redirect(url_for('list_card', card_id=card.card_id))

@app.route("/move_card", methods=['POST'])
@ensure_logged_in
def move_card():
  list_id = request.form.get('list_id', "").strip()
  card_id = request.form.get('card_id', "").strip()

  errors = []

  if len(list_id) == 0:
    errors.append(FieldsNotValidError("List is requried"))
  if len(card_id) == 0:
    errors.append(FieldsNotValidError("Card is requried"))

  if len(list_id) > 0:
    try:
      list_id = int(list_id)
    except:
      errors.append(FieldsNotValidError("List is requried"))

  if len(card_id) > 0:
    try:
      card_id = int(card_id)
    except:
      errors.append(FieldsNotValidError("Card is requried"))

  list_obj = db.session.query(List).filter(List.list_id == list_id).first()
  if list_obj == None:
    errors.append(ResourceNotFound("List with id " + str(list_id) + " does not exist"))

  card_obj = db.session.query(Card).filter(Card.card_id == card_id).first()
  if card_obj == None:
    errors.append(ResourceNotFound("Card with id " + str(card_id) + " does not exist"))

  if len(errors) == 0:
    try:
      card_obj.list = list_obj
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      app.logger.error(e)
      db.session.rollback()
      errors.append(e)
    else:
      app.logger.info('moved card')

  if len(errors) > 0:
    errors = [str(error) for error in errors]
    app.logger.info('Some errors were present : %s', ','.join(errors))
    encoded_redirect_error = create_redirect_error("\n".join(errors))
    return redirect(request.referrer + "?redirect_error={0}".format(encoded_redirect_error))

  return redirect(request.referrer)
