from flask import current_app as app
from flask import render_template

from application.models.list import List

from application.database.index import db
from application.controllers.utils import get_redirect_error, plot_timeline
from application.controllers.decorators import ensure_logged_in

# Board
@app.route("/stats", methods=['GET'])
@ensure_logged_in
def stats():
  errors = []
  redirect_error = get_redirect_error()
  if redirect_error != None:
    errors.append(redirect_error)

  lists = db.session.query(List).all()

  img_hashes = {}

  for l in lists:
    img_hashes[l.list_id] = plot_timeline(l.timeline())

  return render_template('stats/index.html', errors=errors, lists=lists, img_hashes=img_hashes)
