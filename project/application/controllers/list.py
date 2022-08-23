import imp
from flask import current_app as app
from flask import render_template, request, redirect, url_for
from application.models.card import Card
from application.models.list import List

from application.database.index import db

# Board
@app.route("/", methods=['GET'])
def index():
  return "sd"
  # if login ->
  # else -> render_board()
  ...

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
