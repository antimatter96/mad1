from sqlalchemy.orm import relationship

from application.database.index import db

class List(db.Model):
  __tablename__ = 'list'
  list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String)
  description = db.Column(db.String)

  cards = relationship("Card", back_populates="list")

  creator_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
  creator = relationship("User", back_populates="lists")
