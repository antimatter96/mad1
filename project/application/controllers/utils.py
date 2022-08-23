from flask import current_app as app

@app.route("/stats", methods=['GET'])
def stats():
  return "Stats"
