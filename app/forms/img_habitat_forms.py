from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length


class ImgHabitatCreateForm(FlaskForm):
    name = StringField("Nom de l'image",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    filename = FileField("Image", validators=[
            FileRequired(message="Veuillez sélectionner une image."),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Images uniquement !")
        ]
    )
    description = TextAreaField("Description",
        validators=[DataRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Créer")


class ImgHabitatUpdateForm(FlaskForm):
    name = StringField("Nom de l'image",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    filename = FileField("Nouvelle image (optionnel)", validators=[
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Images uniquement !")
        ]
    )
    description = TextAreaField("Description",
        validators=[DataRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Mettre à jour")
