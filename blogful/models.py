import datetime

from .database import db


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024))
    content = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.datetime.now)

db.create_all()
