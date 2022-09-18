import base64

from flask import request
from application.errors import RedirectError

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

def flatten_from_errors(form_errors):
  errors = []
  for k in form_errors:
    errors.extend(form_errors[k])

  return errors
