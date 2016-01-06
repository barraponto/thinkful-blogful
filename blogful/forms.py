from flask_wtf import Form
from wtforms import fields, validators
from wtforms.fields.html5 import EmailField

class EntryForm(Form):
    title = fields.StringField(
        'Title', validators=[validators.InputRequired()])
    content = fields.TextAreaField(
        'Content', validators=[validators.InputRequired()])

class EntryDeleteForm(Form):
    pass

class LoginForm(Form):
    email = EmailField(
        'Email Address',
        validators=[validators.InputRequired(), validators.Email()])
    password = fields.PasswordField(
        'Password', validators=[validators.InputRequired()])
