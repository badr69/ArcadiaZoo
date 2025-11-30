# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileField



# TODO; BaseForm qui fait herite service form
class BaseForm(FlaskForm):
        name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=50)
    ])
        url_image = FileField("Images", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only image files are allowed.")
    ])
        submit = SubmitField("Submit")

# TODO: Formulaire de création de service
class ServiceCreateForm(BaseForm):
        description = TextAreaField("Description", validators=[
        DataRequired(message="Description is required."),
        Length(max=1000, message="Description must be 1000 characters max.")
    ])

# TODO: service Update Form
class ServiceUpdateForm(BaseForm):
        description = TextAreaField("Description", validators=[
        DataRequired(message="Description is required."),
        Length(max=1000, message="Description must be 1000 characters max.")
    ])
