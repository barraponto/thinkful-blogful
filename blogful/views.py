from flask import render_template
from flask.ext.bower import Bower

from . import app
from .models import Entry


Bower(app)


@app.route('/')
def entries():
    entries = Entry.query.order_by(Entry.datetime.desc()).all()
    return render_template('entries.html', entries=entries)
