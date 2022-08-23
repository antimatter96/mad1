from flask import current_app as app, render_template

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
  return render_template('403.html'), 403

from application.controllers.user import *
from application.controllers.card import *
from application.controllers.utils import *
from application.controllers.list import *
