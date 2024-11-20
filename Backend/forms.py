from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    name = StringField(label="Email", validators=[DataRequired()])
    message = TextAreaField(label="Message", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])

class ContactForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    title = StringField(label="Titre", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    submit = SubmitField(label="Submit", validators=[DataRequired()])