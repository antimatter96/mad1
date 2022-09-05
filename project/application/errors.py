class FieldsNotValidError(Exception):
  """Error raised when a field does not feel right"""
  ...

class RedirectError(Exception):
  """Error raised by some other controller"""
  ...

class ResourceNotFound(Exception):
  """Error raised when an object to change is not found"""
  ...
