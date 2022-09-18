import os
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import LocalDevelopmentConfig, TestingConfig

from application.controllers.api.index import api
from application.database.index import db

app = None

def create_app():
  env = os.getenv('ENV', "development")
  app = Flask(__name__, template_folder="templates")
  csrf = CSRFProtect()

  if env == 'production':
    ...
  elif env == 'development':
    app.config.from_object(LocalDevelopmentConfig)
    app.logger.info("Using Local Developlent Config")

    ...
  elif env == 'testing':
    app.config.from_object(TestingConfig)
    ...

  db.init_app(app)
  migrate = Migrate(app, db)
  app.logger.info("migrate")
  csrf.init_app(app)
  api.decorators.append(csrf.exempt)
  api.init_app(app)
  app.app_context().push()
  app.logger.info("App setup complete")

  logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
  return app

app = create_app()
from application.controllers.index import *

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0', port=8080)
