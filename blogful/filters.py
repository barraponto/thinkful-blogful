import mistune
from flask import Markup

from . import app


@app.template_filter()
def markdown(text):
    return Markup(mistune.markdown(text, escape=True))

@app.template_filter()
def dateformat(date, format):
    return date.strftime(format) if date else None
