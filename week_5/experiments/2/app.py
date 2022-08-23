from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1db.sqlite3'
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

##

class User(db.Model):
  __tablename__ = 'user'

  user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  username = db.Column(db.String, unique=True)
  email = db.Column(db.String, unique=True)


class Article(db.Model):
  __tablename__ = 'article'

  ## same name as in db
  article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  title = db.Column(db.String)
  content = db.Column(db.String)

  authors = db.relationship("User", secondary='article_authors')
  # authors = db.relationship("User", secondary='article_authors', lazy='joined') [PREVENT N+1]


class ArticleAuthors(db.Model):
  __tablename__ = 'article_authors'

  user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True, nullable=False)
  article_id = db.Column(db.Integer, db.ForeignKey("article.article_id"), primary_key=True, nullable=False)


# @app.route("/", methods=["GET", "POST"])
# def home():
#   return render_template("base.html")

@app.route("/", methods=["GET", "POST"])
def articles():
  articles = Article.query.all()

  # or
  # articles = db.session.query(Article).all()
  

  #  <td>
  #  {{ article.authors }} <!-- BAD FETCHED ONE BY ONE -->
  #  </td>
  return render_template("articles.html", articles=articles)

@app.route("/articles_by/<user_name>", methods=["GET", "POST"])
def user_articles(user_name):
  articles = Article.query.filter(Article.authors.any(username=user_name)).all()
  return render_template("user_articles.html", articles=articles, username=user_name)

if __name__ == '__main__':
  app.run(
    host='127.0.0.1',
    debug=True,
    port=8080,
  )
