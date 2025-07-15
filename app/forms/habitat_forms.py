# TODO: Importation des dépendances
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.simple import TextAreaField, StringField, FileField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField


# TODO; BaseForm qui fait herite (habitats,animal,services)form
class BaseForm(FlaskForm):
        name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=50)
    ])
        url_image = FileField("Images", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only image files are allowed.")
    ])
        submit = SubmitField("Submit")
# TODO: Formulaire de création d'habitat
class HabitatCreateForm(BaseForm):
        description = TextAreaField("Description", validators=[
        Length(max=300, message="Description must be 300 characters max.")
    ])
        animals = SelectMultipleField("Animals", coerce=int)

# TODO UPDATE FORM HABITATS
class HabitatUpdateForm(BaseForm):
    description = TextAreaField("Description", validators=[
        Length(max=300, message="Description must be 300 characters max.")
    ])
    animals = SelectMultipleField("Animals", coerce=int)
