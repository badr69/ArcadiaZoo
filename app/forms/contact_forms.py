# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email


# TODO: Formulaire de contact
class ContactForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired(message="A title is required"),
        Length(min=4, max=100, message="Title must be between 4 and 100 characters.")
    ])
    email = EmailField("Email", validators=[
        DataRequired(message="Email address is required"),
        Email(message="Email is not valid")
    ])
    description = TextAreaField("Description", validators=[
        DataRequired(message="Description is required."),
        Length(min=10, max=500, message="Description must be at least 10 characters long.")
    ])
    submit = SubmitField("Submit")
