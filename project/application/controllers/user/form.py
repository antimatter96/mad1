from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class SigninForm(FlaskForm):
  password = PasswordField(
      'password',
      validators=[
          DataRequired(message='password is required'),
          Length(min=8, max=32, message="password should be between 8 and 32 characters")
      ]
  )
  username = StringField(
      'username',
      validators=[
          DataRequired(message='Email is required'),
          Email('Invalid Email is'),
          Length(min=5, max=200, message="Email should be between 5 and 200 characters")
      ]
  )

class SignupForm(SigninForm):
  name = StringField(
      'name',
      validators=[DataRequired(message='name is required'),
                  Length(min=1, max=50, message="Name should be between 1 and 50 characters")]
  )
