from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.services.role_service import RoleService

class BaseForm(FlaskForm):
    name = StringField(
        "Nom du rôle",
        validators=[
            DataRequired(message="Le nom du rôle est requis."),
            Length(min=3, max=15)
        ]
    )

class CreateRoleForm(BaseForm):
    submit = SubmitField("Create")

class UpdateRoleForm(BaseForm):
    submit = SubmitField("Update")

class DeleteRoleForm(FlaskForm):
    submit = SubmitField("Delete")
