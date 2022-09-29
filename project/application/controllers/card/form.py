from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Length

class CardForm(FlaskForm):
  title = StringField(
      'title',
      validators=[DataRequired(message='Title is required'),
                  Length(min=1, max=50, message="Title should be between 2 and 50 characters")]
  )
  content = StringField(
      'content',
      validators=[
          DataRequired(message='Summary is required'),
          Length(min=1, max=200, message="Summary should be between 2 and 200 characters")
      ]
  )
  deadline = DateTimeField('deadline', validators=[DataRequired('Deadline is required')], format="%Y-%m-%d")
  list_id = IntegerField('list_id', validators=[DataRequired(message='List is required')])
  complete = BooleanField('complete')

class MoveCardForm(FlaskForm):
  list_id = IntegerField('list_id', validators=[DataRequired(message='List is required')])
  card_id = IntegerField('card_id', validators=[DataRequired(message='Card is required')])
