from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length, length


class CreateRoleForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=15)
    ])
    submit = SubmitField("Submit")

class UpdateRoleForm(FlaskForm):
    name = StringField("Nom du rôle", validators=[
        DataRequired(message="Username is required."),
        length(min=3, max=15)
    ])
    submit = SubmitField("Delete")

class DeleteRoleForm(FlaskForm):
    submit = SubmitField("Confirmer la suppression")


