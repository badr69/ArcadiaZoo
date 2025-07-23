# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

# TODO: Formulaire d'avis / review
class ReviewForm(FlaskForm):
    pseudo = StringField('Pseudo', id='pseudo', validators=[DataRequired()])
    message = TextAreaField('Message', id='text-area-review', validators=[DataRequired()])
    rating = SelectField('Note', choices=[('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')], id='rating', validators=[DataRequired()])
    submit = SubmitField('Envoyer', id='submit-btn')

# class ReviewForm(FlaskForm):
#         pseudo = StringField("Pseudo", validators=[
#         DataRequired(message="The pseudo is required."),
#         Length(min=4, max=20)
#     ])
#         # entity = SelectField(
#         #     choices=[('animals', 'Animals'), ('habitats', 'Habitats'), ('services', 'Services')],
#         #     validators=[DataRequired()]
#         # )
#         message = TextAreaField("Comment", validators=[
#         DataRequired(message="Comment is required."),
#         Length(min=4, max=50)
#     ])
#         rating = IntegerField("Rating (1 to 5)", validators=[
#         DataRequired(message="Please enter a number between 1 and 5")
#     ])
#         submit = SubmitField("Submit")