# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


# TODO: Formulaire de rapport vétérinaire
class ReportForm(FlaskForm):
        animal_status = StringField("Animal's Condition", validators=[
        DataRequired(message="Please enter the animal's condition."),
        Length(min=2, max=100)
    ])
        food = StringField("Proposed Food", validators=[
        DataRequired(message="Please enter the proposed food."),
        Length(min=2, max=100)
    ])
        quantity = DecimalField("Food Quantity (grams)", places=2, validators=[
        DataRequired(message="Please enter the food quantity."),
        NumberRange(min=0.1, message="Quantity must be greater than 0.")
    ])
        visit_date = DateField("Visit Date", format='%Y-%m-%d', validators=[
        DataRequired(message="Please enter the visit date.")
    ])
        submit = SubmitField("Submit")
