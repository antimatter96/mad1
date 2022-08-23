import os
from flask import Flask
from application import config
from application.config import LocalDevConfig
from application.database import db

def create_app():
  app = Flask(__name__, template_folder="templates")

  if os.getenv("ENV", "development") == "production":
    raise Exception("")
  else:
    print("starting local env")
    app.config.from_object(LocalDevConfig)
  db.init_app(app)
  app.app_context().push()
  return app

##

app = create_app()

from application.controllers import *

if __name__ == '__main__':
  app.run(
    host='127.0.0.1',
    debug=True,
    port=8080,
  )
