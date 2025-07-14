# TODO: Importation des dépendances
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField, IntegerField
from wtforms import MultipleFileField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
from flask_wtf.file import FileAllowed, FileField


# from app.utils.validator import StrongPassword


# TODO uploads form
class UploadImageForm(FlaskForm):
    images = MultipleFileField("Uploader des images", validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement !')
    ])
    submit = SubmitField("Envoyer")


class AuthForm(FlaskForm):
        email = StringField("Email", validators=[
        DataRequired(message="Email address is required"),
        Email(message="Email is not valid")
    ])
        password = PasswordField("Password", validators=[
        DataRequired(message="Password is required"),
        Length(min=4, max=25)
    ])

class CreateUserForm(AuthForm):
        username = StringField("Username", validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=15)
    ])
        confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe doivent correspondre.')
    ])

        role_id = SelectField("Role", choices=[
            (2, "Employee"),
            (3, "Vet"),
        ], coerce=int, validators=[DataRequired(message="Please select a role.")])
        submit = SubmitField("Register")

class UpdateUserForm(AuthForm):
        username = StringField('Nom', validators=[DataRequired()])
        role_name = SelectField(
        'Rôle',
        choices=[('employee', 'Employee'), ('vet', 'Vet')],
        validators=[DataRequired()])
        submit = SubmitField('Enregistrer les modifications')

class DeleteUserForm(FlaskForm):
    user_id = IntegerField("ID de l'utilisateur", validators=[
        DataRequired(message="L'ID utilisateur est requis"),
        NumberRange(min=1, message="L'ID doit être un entier positif")
    ])
    submit = SubmitField("Supprimer l'utilisateur")

# TODO: LoginForm
class LoginForm(AuthForm):
    submit = SubmitField("Login")

# TODO: LogoutForm
class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")

# TODO: Formulaire de contact
class ContactForm(AuthForm):
        title = StringField("Title", validators=[
        DataRequired(message="A title is required"),
        Length(min=4, max=100, message="Title must be between 4 and 100 characters.")
    ])
        description = TextAreaField("Description", validators=[
        DataRequired(message="Description is required."),
        Length(min=10, max=500, message="Description must be at least 10 characters long.")
    ])
        submit = SubmitField("Submit")

# TODO; BaseForm qui fait herite (habitats,animal,services)form
class BaseForm(FlaskForm):
        name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=50)
    ])
        url_image = FileField("Images", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only image files are allowed.")
    ])
        submit = SubmitField("Submit")

# TODO: Formulaire de création d'habitat
class HabitatCreateForm(BaseForm):
        description = TextAreaField("Description", validators=[
        Length(max=300, message="Description must be 300 characters max.")
    ])
        animals = SelectMultipleField("Animals", coerce=int)

# TODO UPDATE FORM HABITATS
class HabitatUpdateForm(BaseForm):
    description = TextAreaField("Description", validators=[
        Length(max=300, message="Description must be 300 characters max.")
    ])
    animals = SelectMultipleField("Animals", coerce=int)

# TODO: Formulaire de création d'animal
class AnimalCreateForm(BaseForm):
    race = StringField("Race", validators=[
        DataRequired(message="Race is required."),
        Length(min=2, max=50)
    ])
    description = TextAreaField("Description", validators=[
            Length(max=300, message="Description must be 300 characters max.")
    ])


# TODO: Formulaire de création d'animal
class AnimalUpdateForm(BaseForm):
    race = StringField("Race", validators=[
        DataRequired(message="Race is required."),
        Length(min=2, max=50)
    ])
    description = TextAreaField("Description", validators=[
        Length(max=300, message="Description must be 300 characters max.")
    ])
    # habitat = SelectField("Habitat", coerce=int, validators=[
    #     DataRequired(message="Habitat is required.")
    # ])

# TODO: Formulaire de création de service
class ServiceCreateForm(BaseForm):
        description = TextAreaField("Description", validators=[
        DataRequired(message="Description is required."),
        Length(max=300, message="Description must be 300 characters max.")
    ])

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

# TODO: Formulaire d'avis / review
class ReviewForm(FlaskForm):
        pseudo = StringField("Pseudo", validators=[
        DataRequired(message="The pseudo is required."),
        Length(min=4, max=20)
    ])
        entity = SelectField(
            choices=[('animals', 'Animals'), ('habitats', 'Habitats'), ('services', 'Services')],
            validators=[DataRequired()]
        )
        message = TextAreaField("Comment", validators=[
        DataRequired(message="Comment is required."),
        Length(min=4, max=50)
    ])
        rating = IntegerField("Rating (1 to 5)", validators=[
        DataRequired(message="Please enter a number between 1 and 5")
    ])
        submit = SubmitField("Submit")

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
        submit = SubmitField("Submit")
