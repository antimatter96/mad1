from functools import wraps

from flask import current_app as app
from flask import session, redirect, url_for
from application.models.user import User
from application.models.card import Card
from application.models.list import List
from application.database.index import db
from application.controllers.utils import create_redirect_error

def ensure_card_exists(f):

  @wraps(f)
  def wrapper(*args, **kwds):
    encoded_redirect_error = ""

    card_id = kwds['card_id']
    del kwds['card_id']

    try:
      card_id = int(card_id)
    except:
      encoded_redirect_error = create_redirect_error("Card id required")

    card = None
    if encoded_redirect_error == "":
      card = db.session.query(Card).filter(Card.card_id == card_id).first()
      if card == None:
        encoded_redirect_error = create_redirect_error("Card with id " + str(card_id) + " does not exist")

    if encoded_redirect_error != "":
      return redirect(url_for('render_create_card', redirect_error=encoded_redirect_error))

    print('card ->', card.card_id)
    return f(*args, **kwds, card=card)

  return wrapper

def ensure_list_exists(f):

  @wraps(f)
  def wrapper(*args, **kwds):
    encoded_redirect_error = ""

    list_id = kwds['list_id']
    del kwds['list_id']

    try:
      list_id = int(list_id)
    except:
      encoded_redirect_error = create_redirect_error("List id required")

    list_obj = None
    if encoded_redirect_error == "":
      list_obj = db.session.query(List).filter(List.list_id == list_id).first()
      if list_obj == None:
        encoded_redirect_error = create_redirect_error("List with id " + str(list_id) + " does not exist")

    if encoded_redirect_error != "":
      return redirect(url_for('render_create_list', redirect_error=encoded_redirect_error))

    print('list ->', list_obj.list_id)
    return f(*args, **kwds, list_obj=list_obj)

  return wrapper

def is_logged_in():
  if session is None or 'username' not in session or 'user_id' not in session or \
    session['username'] is None or session['user_id'] is None:
    return False
  return True

def ensure_logged_in(f):

  @wraps(f)
  def wrapper(*args, **kwds):
    if not is_logged_in():
      return redirect(url_for('render_signin'))

    current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    if current_user is None:
      encoded_redirect_error = create_redirect_error("Please login to continue")
      return redirect(url_for('render_signin', redirect_error=encoded_redirect_error))

    print('current_user ->', current_user.user_id)
    return f(*args, **kwds)

  return wrapper

@app.context_processor
def utility_processor():
  return dict(jinja_is_logged_in=is_logged_in)
