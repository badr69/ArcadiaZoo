from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

class BaseForm(FlaskForm):
    """
    Formulaire de base avec les champs communs à tous les formulaires :
    - name
    - description
    - animals
    - image_id
    - submit
    """
    name = StringField("Name", validators=[
        DataRequired(message="Reference is required."),
        Length(min=2, max=50, message="Reference must be between 2 and 50 characters")
    ])
    description = TextAreaField("Description", validators=[Length(max=300)])
    img_hab_id = SelectField("Choose Habitat Image", coerce=int)
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        image_choices = kwargs.pop('image_choices', [])
        super().__init__(*args, **kwargs)
        self.img_hab_id.choices = image_choices


class HabitatCreateForm(BaseForm):
    """
    Formulaire pour créer un habitat.
    Hérite de BaseForm.
    """
    pass  # tous les champs viennent de BaseForm


class HabitatUpdateForm(BaseForm):
    """
    Formulaire pour mettre à jour un habitat.
    Hérite de BaseForm.
    """
    pass  # tous les champs viennent de BaseForm


















# # TODO: Importation des dépendances
# from wtforms.fields.choices import SelectMultipleField
# from wtforms.fields.simple import TextAreaField, StringField, FileField, SubmitField
# from wtforms.validators import Length, DataRequired
# from flask_wtf import FlaskForm
# from flask_wtf.file import FileAllowed, FileField
#
#
# # TODO; BaseForm qui fait herite (habitats,animal,services)form
# class BaseForm(FlaskForm):
#         name = StringField("Name", validators=[
#         DataRequired(message="Name is required."),
#         Length(min=2, max=50)
#     ])
#         url_image = FileField("Images", validators=[
#         FileAllowed(['jpg', 'jpeg', 'png', 'gif'], "Only image files are allowed.")
#     ])
#         submit = SubmitField("Submit")
# # TODO: Formulaire de création d'habitat
# class HabitatCreateForm(BaseForm):
#         description = TextAreaField("Description", validators=[
#         Length(max=300, message="Description must be 300 characters max.")
#     ])
#         animals = SelectMultipleField("Animals", coerce=int)
#
# # TODO UPDATE FORM HABITATS
# class HabitatUpdateForm(BaseForm):
#     description = TextAreaField("Description", validators=[
#         Length(max=300, message="Description must be 300 characters max.")
#     ])
#     animals = SelectMultipleField("Animals", coerce=int)
