# TODO: Importation des dépendances
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

# TODO: Formulaire de commentaire sur un habitat
class HabitatCommentForm(FlaskForm):
        name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=50)
    ])
        status = StringField("State of Habitat", validators=[
        DataRequired(message="State is required."),
        Length(min=4, max=100)
    ])
        improvement = TextAreaField("Improvement and Suggestion", validators=[
        DataRequired(message="Your suggestions are welcome."),
        Length(min=4, max=500)
    ])
        submit= SubmitField("Submit")