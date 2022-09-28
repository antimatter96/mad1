from flask_restful import current_app as app
from flask_restful import Resource, reqparse, inputs, fields, marshal_with

from application.controllers.api.utils import token_required
from application.database.index import db
from application.models.card import Card
from application.models.list import List
from application.controllers.api.errors import NotFoundError, BusinessValidationError, InternalServerError, common_errors
from application.controllers.api.utils import min_length

class SimpleDateTime(fields.Raw):

  def format(self, value):
    return value.strftime('%Y-%m-%d')

list_errors = {
    "list_001": "List does not exist",
    "list_002": "Target list_id required",
    "list_003": "Target List does not exist",
    "list_004": "Target List cannot be same as list to delete",
}

list_fields = {
    "list_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
}

list_update_parser = reqparse.RequestParser()
list_update_parser.add_argument('description', type=min_length(1), required=True)
list_update_parser.add_argument('name', type=min_length(1), required=True)
list_create_parser = list_update_parser.copy()

list_delete_parser = reqparse.RequestParser()
list_delete_parser.add_argument('mode', choices=('move', 'delete'), required=True)
list_delete_parser.add_argument('list_id', type=int)

class ListAPI(Resource):
  method_decorators = [token_required]

  @marshal_with(list_fields)
  def get(self, current_user, list_id):
    list_obj = db.session.query(List).filter(List.list_id == list_id).first()
    if list_obj is None:
      raise NotFoundError(error_code='list_001', error_message=list_errors['list_001'])

    return list_obj, 200

  def delete(self, current_user, list_id):
    list_obj = db.session.query(List).filter(List.list_id == list_id).first()
    if list_obj is None:
      raise NotFoundError(error_code='list_001', error_message=list_errors['list_001'])

    args = list_delete_parser.parse_args()

    mode = args.get('mode')
    if mode == "move":
      new_list_id = args.get('list_id')
      if new_list_id == None:
        raise BusinessValidationError(status_code=400, error_code='list_002', error_message=list_errors['list_002'])

      new_list_obj = db.session.query(List).filter(List.list_id == new_list_id).first()
      if new_list_obj is None:
        raise NotFoundError(error_code='list_002', error_message=list_errors['list_002'])

      if new_list_obj.list_id == list_obj.list_id:
        raise BusinessValidationError(status_code=400, error_code='list_004', error_message=list_errors['list_004'])

    if mode == "delete":
      try:
        for card in list_obj.cards:
          db.session.delete(card)
        db.session.flush()
        db.session.delete(list_obj)
        db.session.commit()
      except Exception as e:
        app.log_exception(e)
        app.logger.error(e)
        db.session.rollback()
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
      else:
        app.logger.info('list deleted')

    return '', 200

  @marshal_with(list_fields)
  def put(self, current_user, list_id):
    list_obj = db.session.query(List).filter(List.list_id == list_id).first()
    if list_obj == None:
      raise NotFoundError(error_code='list_001', error_message=list_errors['list_001'])

    args = list_update_parser.parse_args()

    name = args.get('name')
    description = args.get('description')

    try:
      list_obj.name = name
      list_obj.description = description
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return list_obj

  @marshal_with(list_fields)
  def post(self, current_user):
    args = list_create_parser.parse_args()

    name = args.get('name')
    description = args.get('description')

    try:
      new_list = List(name=name, description=description, creator=current_user)
      db.session.add(new_list)
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return new_list
