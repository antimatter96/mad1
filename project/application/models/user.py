from datetime import datetime
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

  auth_token = db.Column(db.String(255))

  created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
