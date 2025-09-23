# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms import SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo


class BaseForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(message="Email address is required"),
        Email(message="Email is not valid")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required"),
        Length(min=4, max=25)
    ])
    confirm_password = PasswordField("Password", validators=[
        DataRequired(message="Password is required"),
        Length(min=4, max=25)
    ])
    submit = SubmitField("Create User")

class CreateUserForm(BaseForm):
        username = StringField("Username", validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=15)
    ])
        confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe doivent correspondre.')
    ])

        role_name = SelectField("Rôle", validators=[DataRequired()], choices=[])  # ← dynamique

class UpdateUserForm(BaseForm):
        username = StringField('Nom', validators=[DataRequired()])
        role_name = SelectField(
        'Rôle',
        choices=[('employee', 'Employee'), ('vet', 'Vet')],
        validators=[DataRequired()])
        submit = SubmitField('Submit')

class DeleteUserForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[
        DataRequired(message="User ID Required"),
        NumberRange(min=1, message="ID must be a int")
    ])
    submit = SubmitField("Delete User")
