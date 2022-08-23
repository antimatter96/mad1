from functools import wraps

from flask import current_app as app
from flask import session, redirect, url_for
from application.models.user import User
from application.database.index import db
from application.errors import FieldsNotValidError

def is_logged_in():
  if session is None or 'username' not in session or 'user_id' not in session or \
    session['username'] is None or session['user_id'] is None:
    return False
  return True

def log_session(f):

  @wraps(f)
  def wrapper(*args, **kwds):
    print(session)
    return f(*args, **kwds)

  return wrapper

def add_user(f):

  @wraps(f)
  def wrapper(*args, **kwds):
    if not is_logged_in():
      return redirect(url_for('render_signin'))

    current_user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    if current_user is None:
      return redirect(url_for('render_signin'))

    return f(current_user, *args, **kwds)

  return wrapper
