from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateRoleForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=15)
    ])
    submit = SubmitField("Submit")