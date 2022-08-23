import imp
from flask import current_app as app
from flask import render_template, request, redirect, url_for, session
from application.models.card import Card
from application.models.list import List

from application.database.index import db

from application.controllers.utils import add_user

# Board
@app.route("/", methods=['GET'])
@add_user
def index(current_user):
  lists = db.session.query(Card).all()
  return render_template('board/index.html', errors=[], lists=[{'index': 1}, {'index': 2}])
  # if login ->
  # else -> render_board()

# Lists
@app.route("/list", methods=['POST'])
def create_list():
  return "_list_students"

@app.route("/list/<list_id>", methods=['DELETE'])
def delete_list(list_id):
  return "_list_students"

@app.route("/list/<list_id>", methods=['PUT'])
def edit_list():
  return "_list_students"
