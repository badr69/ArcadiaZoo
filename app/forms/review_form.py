# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

# TODO: Formulaire d'avis / review
class ReviewForm(FlaskForm):
    pseudo = StringField('Pseudo', id='pseudo', validators=[DataRequired()])
    message = TextAreaField('Message', id='text-area-review', validators=[DataRequired()])
    rating = SelectField('Note', choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')], id='rating', validators=[DataRequired()])
    submit = SubmitField('Envoyer', id='submit-btn')
