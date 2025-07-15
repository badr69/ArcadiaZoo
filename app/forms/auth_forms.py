# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class AuthForm(FlaskForm):
        email = StringField("Email", validators=[
        DataRequired(message="Email address is required"),
        Email(message="Email is not valid")
    ])
        password = PasswordField("Password", validators=[
        DataRequired(message="Password is required"),
        Length(min=4, max=25)
    ])

# TODO: LoginForm
class LoginForm(AuthForm):
    submit = SubmitField("Login")

# TODO: LogoutForm
class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")