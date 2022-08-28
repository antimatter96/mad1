from sqlalchemy.orm import relationship

from application.database.index import db

class User(db.Model):
  __tablename__ = 'user'
  user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  username = db.Column(db.String, unique=False)
  name = db.Column(db.String, unique=False)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())

  cards = relationship("Card", back_populates="creator")
  lists = relationship("List", back_populates="creator")

  def display_name(__self__):
    return __self__.username.split('@')[0]
