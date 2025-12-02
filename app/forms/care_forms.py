from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired
from app.services.animal_service import AnimalService
from app.services.user_service import UserService  # pour récupérer les vétérinaires


class BaseCareForm(FlaskForm):
    """
    Formulaire de base pour Care : animal, vétérinaire, type, description et date.
    """
    animal_id = SelectField("Animal", coerce=int, validators=[DataRequired()])
    user_id = SelectField("Vétérinaire", coerce=int, validators=[DataRequired()])
    type_care = StringField("Type de soin", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    date_care = DateField("Date du soin", format="%Y-%m-%d", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplir dynamiquement les choix d'animaux
        self.animal_id.choices = [(a.animal_id, a.name) for a in AnimalService.list_all_animals()]
        # Remplir dynamiquement les choix de vétérinaires
        self.user_id.choices = [("", "— Choisir un vétérinaire —")] + [
            (u.user_id, u.username) for u in UserService.list_all_vets()
        ]
        vets = UserService.list_all_vets()
        self.user_id.choices = [(u.user_id, u.username) for u in vets]

        if not vets:
            self.user_id.choices = [("", "Aucun vétérinaire disponible")]


class CareCreateForm(BaseCareForm):
    """
    Formulaire pour créer un nouveau care.
    """
    submit = SubmitField("Créer le soin")


class CareUpdateForm(BaseCareForm):
    """
    Formulaire pour mettre à jour un care existant.
    """
    submit = SubmitField("Mettre à jour le soin")
