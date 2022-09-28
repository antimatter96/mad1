from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from application.database.index import db

class Card(db.Model):
  __tablename__ = 'card'
  card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.Text, nullable=False)
  deadline = db.Column(db.DateTime, nullable=False)
  completed_on = db.Column(db.DateTime, nullable=True)
  complete = db.Column(db.Boolean, nullable=False, default=False)

  parent_id = db.Column(db.Integer, db.ForeignKey("list.list_id"))
  list = relationship("List", back_populates="cards")

  creator_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
  creator = relationship("User", back_populates="cards")

  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

  @hybrid_property
  def deadline_passed(self):
    if self.complete:
      return self.completed_on > self.deadline
    return datetime.now() > self.deadline
