import json

from werkzeug.exceptions import HTTPException
from flask import make_response

class NotFoundError(HTTPException):

  def __init__(self, error_code, error_message):
    data = {"error_code": error_code, "error_message": error_message}
    self.response = make_response(json.dumps(data), 404)

class BusinessValidationError(HTTPException):

  def __init__(self, status_code, error_code, error_message):
    data = {"error_code": error_code, "error_message": error_message}
    self.response = make_response(json.dumps(data), status_code)

class InternalServerError(HTTPException):

  def __init__(self, error_code, error_message):
    data = {"error_code": error_code, "error_message": error_message}
    self.response = make_response(json.dumps(data), 500)

class AuthenticationError(HTTPException):

  def __init__(self, error_code, error_message):
    data = {"error_code": error_code, "error_message": error_message}
    self.response = make_response(json.dumps(data), 401)

common_errors = {
    "common_001": "Some error occured",
}
