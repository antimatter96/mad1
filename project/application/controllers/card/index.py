from datetime import datetime

from flask import current_app as app
from flask import render_template, request, redirect, url_for, session

from application.models.card import Card
from application.models.list import List
from application.models.user import User

from application.database.index import db
from application.errors import FieldsNotValidError, ResourceNotFound
from application.controllers.utils import get_redirect_error, create_redirect_error, flatten_from_errors
from application.controllers.decorators import ensure_card_exists, ensure_logged_in
from application.controllers.card.form import CardForm, MoveCardForm

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
  form = CardForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  list_id = form.list_id.data

  new_card = None
  if len(errors) == 0:
    title = form.title.data
    content = form.content.data
    deadline = form.deadline.data
    complete = form.complete.data

    app.logger.info('Searcing for user')
    current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    current_list = db.session.query(List).filter(List.list_id == list_id).first()
    if current_list != None:
      try:
        new_card = Card(title=title, content=content, deadline=deadline, complete=complete, creator=current_user, list=current_list)
        if complete:
          new_card.completed_on = datetime.now()
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

  return redirect(url_for('render_card', card_id=new_card.card_id))

@app.route("/card/<card_id>/delete", methods=['POST'])
@ensure_logged_in
@ensure_card_exists
def delete_card(card):
  errors = []
  try:
    db.session.delete(card)
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
    return redirect(url_for('render_edit_card', card_id=card.card_id, redirect_error=encoded_redirect_error))

  return redirect(url_for('index'))

@app.route("/card/<card_id>", methods=['GET'])
@ensure_logged_in
@ensure_card_exists
def render_card(card):
  return render_template('cards/card.html', errors=[], card=card)

@app.route("/card/<card_id>/edit", methods=['GET'])
@ensure_logged_in
@ensure_card_exists
def render_edit_card(card):
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  lists = db.session.query(List).with_entities(List.list_id, List.name).all()

  return render_template('cards/edit_card.html', errors=errors, lists=lists, card=card)

@app.route("/card/<card_id>/edit", methods=['POST'])
@ensure_logged_in
@ensure_card_exists
def edit_card(card):
  form = CardForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  update_completed_time = False
  if len(errors) == 0:
    if card.complete == False and form.complete.data == True:
      update_completed_time = True

    list_id = form.list_id.data

    app.logger.info('Searcing for user')
    current_list = db.session.query(List).filter(List.list_id == list_id).first()
    if current_list != None:
      try:
        card.title = form.title.data
        card.content = form.content.data
        card.deadline = form.deadline.data
        card.list = current_list
        if update_completed_time:
          card.complete = True
          card.completed_on = datetime.now()
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
    return redirect(url_for('render_edit_card', card_id=card.card_id, redirect_error=encoded_redirect_error))

  return redirect(url_for('render_card', card_id=card.card_id))

@app.route("/move_card", methods=['POST'])
@ensure_logged_in
def move_card():
  form = MoveCardForm()
  form.validate()
  errors = flatten_from_errors(form.errors)

  list_id = form.list_id.data
  card_id = form.card_id.data

  list_obj = None
  card_obj = None
  if len(errors) == 0:
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
