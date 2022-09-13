from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length

class ListForm(FlaskForm):
  name = StringField(
      'name',
      validators=[DataRequired(message='Name is required'),
                  Length(min=1, max=20, message="Name should be between 2 and 20 characters")]
  )
  description = StringField(
      'description',
      validators=[
          DataRequired(message='description is required'),
          Length(min=1, max=50, message="Name should be between 2 and 50 characters")
      ]
  )

class DeleteListForm(FlaskForm):

  def validate_new_list_id(form, field):
    if (len(form.form_errors) == 0 and form.mode.data == 'move'):
      if (field.data == None):
        raise ValidationError("List is requried")

  mode = SelectField(
      'mode',
      choices=[("move", "move"), ("delete", "delete")],
  )
  list_id = IntegerField('list_id', validators=[validate_new_list_id])
