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
    submit = SubmitField("Créer l'utilisateur")

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
        submit = SubmitField('Enregistrer les modifications')

class DeleteUserForm(FlaskForm):
    user_id = IntegerField("ID de l'utilisateur", validators=[
        DataRequired(message="L'ID utilisateur est requis"),
        NumberRange(min=1, message="L'ID doit être un entier positif")
    ])
    submit = SubmitField("Supprimer l'utilisateur")
