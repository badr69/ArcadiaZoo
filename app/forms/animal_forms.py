# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from flask_wtf.file import FileAllowed, FileField


# TODO; BaseForm qui fait herite animalform
class BaseForm(FlaskForm):
        name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=50)
    ])
        url_image = FileField("Images", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only image files are allowed.")
    ])
        submit = SubmitField("Submit")

# TODO: Formulaire de création d'animal
class AnimalCreateForm(BaseForm):
    race = StringField("Race", validators=[
        DataRequired(message="Race is required."),
        Length(min=2, max=50)
    ])
    description = TextAreaField("Description", validators=[
            Length(max=300, message="Description must be 300 characters max.")
    ])

# TODO: Formulaire de création d'animal
class AnimalUpdateForm(BaseForm):
    race = StringField("Race", validators=[
        DataRequired(message="Race is required."),
        Length(min=2, max=50)
    ])
    description = TextAreaField("Description", validators=[
        Length(max=300, message="Description must be 300 characters max.")
    ])

