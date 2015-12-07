from flask_wtf import Form
from wtforms import fields, validators

class EntryForm(Form):
    title = fields.StringField('Title', validators=[validators.InputRequired()])
    content = fields.TextAreaField('Content', validators=[validators.InputRequired()])
