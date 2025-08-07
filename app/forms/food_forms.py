from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DecimalField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from datetime import datetime

class FoodForm(FlaskForm):
    animal = SelectField('Animal', coerce=int, validators=[DataRequired()])
    type_food = StringField('food type', validators=[DataRequired(), Length(max=100)])
    quantity = DecimalField('Quantity (en kg ou L)', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    date_food = DateTimeField('Date/hour', default=datetime.now, format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Submit')
