from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired
from app.services.animal_service import AnimalService
from app.services.user_service import UserService

CARE_TYPES = [("Vaccination", "Vaccination"), ("Check-up", "Check-up"), ("Soin mineur", "Soin mineur")]

class CareCreateForm(FlaskForm):
    animal_id = SelectField("Animal", coerce=int, validators=[DataRequired()])
    vet_id = SelectField("Vétérinaire", coerce=int, validators=[DataRequired()])
    type_care = SelectField("Type de soin", choices=CARE_TYPES, validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    date_care = DateField("Date du soin", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Créer le soin")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplir dynamiquement les options
        self.animal_id.choices = [(a.id, a.name) for a in AnimalService.list_all_animals()]
        self.vet_id.choices = [(v.id, v.username) for v in UserService.list_all_vets()]


class CareUpdateForm(FlaskForm):
    animal_id = SelectField("Animal", coerce=int, validators=[DataRequired()])
    vet_id = SelectField("Vétérinaire", coerce=int, validators=[DataRequired()])
    type_care = SelectField("Type de soin", choices=CARE_TYPES, validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    date_care = DateField("Date du soin", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Mettre à jour le soin")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplir dynamiquement les choix
        self.animal_id.choices = [(a.id, a.name) for a in AnimalService.list_all_animals()]
        self.vet_id.choices = [(v.id, v.username) for v in UserService.list_all_vets()]



