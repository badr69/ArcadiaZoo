from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

class BaseImgForm(FlaskForm):
    """
    Formulaire de base pour les images, contenant les champs communs.
    """
    filename = FileField("Image", validators=[
        FileAllowed(["jpg", "jpeg", "png", "gif"], "Images uniquement !")
    ])
    description = TextAreaField("Description",
        validators=[DataRequired(), Length(min=5, max=500)]
    )
    habitat_id = SelectField("Habitat", coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """
        Permet de passer les choices dynamiques pour le SelectField.
        """
        habitat_choices = kwargs.pop("habitat_choices", [])
        super().__init__(*args, **kwargs)
        self.habitat_id.choices = habitat_choices


class ImgHabitatCreateForm(BaseImgForm):
    """
    Formulaire pour créer une image d'habitat.
    Le champ 'filename' est obligatoire ici.
    """
    submit = SubmitField("Créer")


class ImgHabitatUpdateForm(BaseImgForm):
    """
    Formulaire pour mettre à jour une image d'habitat.
    Le champ 'filename' est optionnel.
    """
    submit = SubmitField("Mettre à jour")
