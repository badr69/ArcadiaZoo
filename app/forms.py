# TODO importation des dependences
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_wtf.file import FileAllowed, MultipleFileField
from .submit_mixin import SubmitMixin


# TODO Baseform qui hetir de SubmitMixin
class BaseForm(FlaskForm, SubmitMixin):
    pass

# TODO Authform aui fait herite d'autres formulaires(register, login et logout.
class AuthForm(BaseForm):
    email = StringField("Email", validators=[DataRequired(message="email adresse is required"),
                                             Email(message="email is not valid")])
    password = PasswordField("password", validators=[DataRequired(message="password is required"),
                                                     Length(min=4, max=25)])

# TODO Register form qui herite de AuthForm
class RegisterForm(AuthForm):
    username = StringField("username",
                           validators=[DataRequired(message="username is required."), Length(min=3, max=15)])

# TODO Login from qui herite de BAseForm
class Loginforrm(BaseForm):
    pass

# TODO Logout form
class LogoutForm(BaseForm):
    pass

# -----------------Contact form-----------------
# TODO Contact form
class ContactForm(SubmitMixin):
    title = StringField("Title", validators=[DataRequired(message="a title is required"), Length(min=4, max=100,
                                                                                                 message="Title must be between 3 and 100 characters.")])
    description = TextAreaField("Description", validators=[
        DataRequired(message="Description is required."),
        Length(min=10, message="Description must be at least 10 characters long.")
    ])

# TODO Create HabitatsForm
class HabitatCreateForm(FlaskForm, SubmitMixin):
    name = StringField("Name", validators=[
        DataRequired(message="name is required."),
        Length(min=2, max=50, message="Name must be between 2 and 50 characters.")])
    description = TextAreaField("Description",
                                validators=[Length(max=300, message="Description must be 300 characters max.")])
    images = MultipleFileField("Images", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only images are allowed.")])

# TODO Create Animalsform
class AnimalCreateForm(FlaskForm, SubmitMixin):
    name = StringField("name", validators=[DataRequired(message="name is required."),
                                           Length(min=2, max=50, message="Name must be between 2 and 50 characters.")])
    race = StringField("Race", validators=[DataRequired(message="race is required."),
                                           Length(min=2, max=50, message="Name must be between 2 and 50 characters.")])
    images = MultipleFileField("Images", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only images are allowed.")])
    habitat = SelectField("Habitat", coerce=int, validators=[DataRequired(message="habitat is required.")])

# TODO Create Services form
class ServicecreateForm(FlaskForm, SubmitMixin):
    name = StringField("name", validators=[DataRequired(message="name is required."),
                                           Length(min=2, max=50, message="Name must be between 2 and 50 characters.")])
    description = TextAreaField("Description", validators=[DataRequired, Length(max=300,
                                                                                message="Description must be 300 characters max.")])
# TODO create Rapport Veterinaire form
class ServiceForm(FlaskForm):
    animal_status = StringField("Animal's Condition",
                                validators=[DataRequired(message="Please enter the animal's condition."),
                                            Length(min=2, max=100)])
    food = StringField("Proposed Food",
                       validators=[DataRequired(message="Please enter the proposed food."), Length(min=2, max=100)])
    quantity = DecimalField("Food Quantity (grams)", places=2,
                            validators=[DataRequired(message="Please enter the food quantity."),
                                        NumberRange(min=0.1, message="Quantity must be greater than 0.")])
    visit_date = DateField("Visit Date", format='%Y-%m-%d',
                           validators=[DataRequired(message="Please enter the visit date.")])

# TODO AVISFORMS
class ReviewForm(FlaskForm, SubmitMixin):
    pseudo = StringField("pseudo", validators=[DataRequired(message="the pseudo is required."), Length(min=4, max=20)])
    comment = TextAreaField("Comment",
                            validators=[DataRequired(message="Please enter the proposed food."), Length(min=4, max=50)])
    rating = IntegerField("Note (1 à 5)", validators=[DataRequired(message="please enter a number between 1 and 5")])

# TODO HabitatCommentform
class HabitatCommentForm(FlaskForm, SubmitMixin):
    name = StringField("name", validators=[DataRequired(message="name is required."),
                                           Length(min=2, max=50, message="Name must be between 2 and 50 characters.")])
    status = StringField("State of habitat",
                         validators=[DataRequired(message="state required."), Length(min=4, max=100)])
    improvement = TextAreaField("Improvement and suggestion",
                                validators=[DataRequired(message="you suggestion are welcom"), Length(min=4, max=500)])
