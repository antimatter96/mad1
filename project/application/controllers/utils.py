import base64
from functools import wraps

from flask import current_app as app
from flask import session, request
from application.errors import RedirectError

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

def create_redirect_error(error_str):
  return base64.b64encode(bytes(error_str, "utf-8")).decode("utf-8")

def get_redirect_error():
  encoded_redirect_error = request.args.get('redirect_error', "").strip()
  if encoded_redirect_error != "":
    try:
      decored_redirect_error = base64.b64decode(encoded_redirect_error).decode("utf-8")
      return RedirectError(decored_redirect_error)
    except:
      return None

  return None
