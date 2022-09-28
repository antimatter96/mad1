from functools import wraps

from flask_restful import request

from application.models.user import User

from application.database.index import db
from application.controllers.api.errors import AuthenticationError, InternalServerError, common_errors

auth_errors = {"auth_001": "Token not present", "auth_002": "Invalid Token", "auth_003": "API Token Invalid or Does not exist"}

def token_required(f):

  @wraps(f)
  def decorator(*args, **kwargs):
    token = None

    if 'x-api-token' in request.headers:
      token = request.headers['x-api-token']

    if not token:
      raise AuthenticationError(error_code='auth_001', error_message=auth_errors['auth_001'])
    if len(token) != 64:
      raise AuthenticationError(error_code='auth_002', error_message=auth_errors['auth_002'])

    try:
      current_user = db.session.query(User).filter(User.auth_token == token).first()
    except:
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    if current_user == None:
      raise AuthenticationError(error_code='auth_003', error_message=auth_errors['auth_003'])

    return f(current_user, *args, **kwargs)

  return decorator

def min_length(min_length):
  def validate(s):
      if type(s) is not str:
        raise ValueError("Must be at least {0} characters long".format(min_length))
      if len(s) >= min_length:
          return s
      raise ValueError("Must be at least {0} characters long".format(min_length))
  return validate
