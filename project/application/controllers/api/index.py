from flask_restful import Api

from application.controllers.api.card import CardAPI
from application.controllers.api.list import ListAPI

api = Api()
api.add_resource(CardAPI, "/api/card", "/api/card/<int:card_id>")
api.add_resource(ListAPI, "/api/list", "/api/list/<int:list_id>")
