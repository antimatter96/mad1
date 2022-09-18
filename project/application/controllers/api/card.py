from datetime import datetime
from flask_restful import current_app as app

from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse, inputs

from application.controllers.api.utils import token_required
from application.database.index import db
from application.models.card import Card
from application.models.list import List
from application.controllers.api.errors import NotFoundError, BusinessValidationError, InternalServerError, common_errors

class SimpleDateTime(fields.Raw):

  def format(self, value):
    return value.strftime('%Y-%m-%d')

card_errors = {
    "card_001": "List does not exist",
    "card_009": "Card does not exist",
}

card_fields = {
    "card_id": fields.Integer,
    "list_id": fields.Integer(attribute='parent_id'),
    "creator_id": fields.Integer,
    "deadline": SimpleDateTime,
    "completed_on": SimpleDateTime,
    "title": fields.String,
    "content": fields.String,
    "complete": fields.Boolean,
}

card_update_parser = reqparse.RequestParser()
card_update_parser.add_argument('title', type=str, required=True)
card_update_parser.add_argument('content', type=str, required=True)
card_update_parser.add_argument('complete', type=inputs.boolean, default=False)
card_update_parser.add_argument('list_id', type=int, required=True)
card_update_parser.add_argument('deadline', type=inputs.date, required=True)
card_create_parser = card_update_parser.copy()

class CardAPI(Resource):
  method_decorators = [token_required]

  @marshal_with(card_fields)
  def get(self, current_user, card_id):
    card = db.session.query(Card).filter(Card.card_id == card_id).first()
    if card is None:
      raise NotFoundError(error_code='card_009', error_message=card_errors['card_009'])

    return card, 200

  def delete(self, current_user, card_id):
    card = db.session.query(Card).filter(Card.card_id == card_id).first()
    if card is None:
      raise NotFoundError(error_code='card_009', error_message=card_errors['card_009'])

    try:
      db.session.delete(card)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return '', 200

  @marshal_with(card_fields)
  def put(self, current_user, card_id):
    card = db.session.query(Card).filter(Card.card_id == card_id).first()
    if card is None:
      raise NotFoundError(error_code='card_009', error_message=card_errors['card_009'])

    args = card_update_parser.parse_args()

    title = args.get('title')
    content = args.get('content')
    complete = args.get('complete', False)
    deadline = args.get('deadline')
    list_id = args.get('list_id')
    update_completed_time = False
    if card.complete == False and complete == True:
      update_completed_time = True

    list_obj = db.session.query(List).filter(List.list_id == list_id).first()
    if list_obj == None:
      raise BusinessValidationError(status_code=400, error_code='card_001', error_message=card_errors['card_001'])

    try:
      card.title = title
      card.content = content
      card.deadline = deadline
      card.complete = complete
      card.list = list_obj
      if update_completed_time:
        card.completed_on = datetime.now()
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return card

  @marshal_with(card_fields)
  def post(self, current_user):
    args = card_create_parser.parse_args()

    title = args.get('title')
    content = args.get('content')
    complete = args.get('complete', False)
    deadline = args.get('deadline')
    list_id = args.get('list_id')

    list_obj = db.session.query(List).filter(List.list_id == list_id).first()
    if list_obj == None:
      raise BusinessValidationError(status_code=400, error_code='card_001', error_message=card_errors['card_001'])


    try:
      new_card = Card(title=title, content=content, deadline=deadline, complete=complete, creator=current_user, list=list_obj)
      if complete:
        new_card.completed_on = datetime.now()
      db.session.add(new_card)
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return new_card
