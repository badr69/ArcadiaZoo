# app/forms/food_forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.services.animal_service import AnimalService
from app.services.user_service import UserService  # pour les vets/employees


# =========================
# BASE FORM
# =========================
class BaseFoodForm(FlaskForm):
    animal_id = SelectField("Animal", coerce=int, validators=[DataRequired()])
    vet_id = SelectField("Vet", coerce=int, validators=[DataRequired()])
    employee_id = SelectField("Employee", coerce=int, validators=[DataRequired()])
    name_food = StringField("Name of food", validators=[DataRequired(), Length(max=100)])
    quantity = DecimalField(
        "Quantity (kg)",
        places=2,
        validators=[DataRequired(), NumberRange(min=0.01)]
    )
    date_food = DateField(
        "Date of food",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remplir dynamiquement les choix pour animal
        animals = AnimalService.list_all_animals()
        self.animal_id.choices = [(a.animal_id, a.name) for a in animals]

        # Vétérinaires
        vets = UserService.list_all_vets()
        self.vet_id.choices = [(u.user_id, u.username) for u in vets]

        # Employés
        employees = UserService.list_all_employees()
        self.employee_id.choices = [(u.user_id, u.username) for u in employees]


# =========================
# CREATE FORM
# =========================
class FoodCreateForm(BaseFoodForm):
    """Formulaire pour créer un enregistrement de nourriture."""
    pass


# =========================
# UPDATE FORM
# =========================
class FoodUpdateForm(BaseFoodForm):
    """Formulaire pour mettre à jour un enregistrement de nourriture."""
    pass
