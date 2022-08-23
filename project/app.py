import os
from flask import Flask, render_template
from flask_migrate import Migrate

from application.database.index import db
from config import LocalDevelopmentConfig, TestingConfig


import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = None

def create_app():
  env = os.getenv('ENV', "development")
  app = Flask(__name__, template_folder="templates")

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
  app.app_context().push()
  app.logger.info("App setup complete")
  return app

app = create_app()
from application.controllers.index import *


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0', port=8080)
