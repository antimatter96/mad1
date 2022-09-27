from datetime import date, datetime, timedelta
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from application.database.index import db

class List(db.Model):
  __tablename__ = 'list'
  list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String)
  description = db.Column(db.String)

  cards = relationship("Card", back_populates="list")

  creator_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
  creator = relationship("User", back_populates="lists")

  created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)

  @hybrid_property
  def count_completed(self):
    return sum([card.complete for card in self.cards])

  @hybrid_property
  def count_missed_deadline(self):
    return sum([card.deadline_passed for card in self.cards])

  def timeline(self):
    from_time = min([card.created_at for card in self.cards])

    timeline_arr = []

    time_slice = (datetime.now() - from_time)
    time_slice = time_slice.seconds/(60*10)

    while from_time < datetime.now():
      total = sum([card.created_at <= from_time for card in self.cards])
      completed = sum(
          [card.created_at <= from_time and card.completed_on is not None and card.completed_on <= from_time for card in self.cards]
      )
      missed = sum(
          [
              card.created_at <= from_time and (
                  (card.deadline <= from_time and card.completed_on is None) or
                  (card.deadline <= from_time and card.completed_on is not None and card.completed_on > card.deadline)
              ) for card in self.cards
          ]
      )

      timeline_arr.append({
          'time': from_time.strftime('%y-%m-%d %H:%M'),
          'total': total,
          'completed': completed,
          'missed': missed,
      })

      from_time = from_time + timedelta(minutes=30)
    return timeline_arr
