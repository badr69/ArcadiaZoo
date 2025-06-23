from wtforms.fields.simple import SubmitField


class SubmitMixin():
    submit = SubmitField("Submit")