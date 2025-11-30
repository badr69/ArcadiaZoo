from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.services.role_service import RoleService
from app.utils.security import sanitize_html

class BaseUserForm(FlaskForm):
    username = StringField(
        "Nom d'utilisateur",
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(), EqualTo('password', message="Les mots de passe ne correspondent pas.")]
    )
    role_id = SelectField("Rôle", coerce=int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        roles = RoleService.list_all_roles()
        self.role_id.choices = [(role.id, role.name) for role in roles]

class CreateUserForm(BaseUserForm):
    submit = SubmitField("Créer")

class UpdateUserForm(BaseUserForm):
    submit = SubmitField("Mettre à jour")

class DeleteUserForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    submit = SubmitField("Confirmer la suppression")
