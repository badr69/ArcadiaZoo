# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileField

from app.services.habitat_service import HabitatService


# TODO; BaseForm qui fait herite animalform
class BaseAnimalForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(), Length(min=2, max=50)])
    race = StringField("Race", validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField("Description", validators=[Length(max=300)])
    url_image = FileField("Image", validators=[FileAllowed(['jpg','jpeg','png','gif'])])
    habitat = SelectField("Habitat", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        habitats = HabitatService.list_all_habitats()
        self.habitat.choices = [(h.habitat_id, h.name) for h in habitats]

# TODO: Formulaire de création d'animal
class AnimalCreateForm(BaseAnimalForm):
    pass

# TODO: Formulaire de création d'animal
class AnimalUpdateForm(BaseAnimalForm):
    pass





