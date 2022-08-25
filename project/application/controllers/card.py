import imp
from flask import current_app as app
from flask import render_template, request, redirect, url_for
from application.models.card import Card
from application.models.list import List

from application.database.index import db

@app.route("/card/all", methods=['GET'])
def cards():
  cards = db.session.query(Card).filter()
  return cards

@app.route("/card", methods=['GET'])
def render_create_card():
  lists = db.session.query(List).with_entities(List.list_id, List.name).all()

  return render_template('board/new_card.html', errors=[])
  return lists

@app.route("/card", methods=['POST'])
def create_card():
  print(request.form)
  roll_no = request.form.get('roll')
  f_name = request.form.get('f_name')
  l_name = request.form.get('l_name')

  return None

@app.route("/card/<card_id>", methods=['DELETE'])
def delete_card(card_id):
  return '_list_students'

@app.route("/card/<card_id>", methods=['PUT'])
def edit_card(card_id):
  return '_list_students()'

@app.route("/card/<card_id>", methods=['GET'])
def list_card(card_id):
  return '_list_students'

@app.route("/move_card", methods=['POST'])
def move_card():
  ...

@app.route("/list_orphans", methods=['GET'])
def list_orphans():
  ...

@app.route("/stats", methods=['GET'])
def stats():
  return "Stats"
