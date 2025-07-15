# TODO: Importation des dépendances
from flask_wtf import  FlaskForm
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

# TODO uploads form
class UploadImageForm(FlaskForm):
    images = MultipleFileField("Uploader des images", validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement !')
    ])
    submit = SubmitField("Envoyer")