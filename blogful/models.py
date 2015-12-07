import datetime

from flask.ext.login import UserMixin

from .database import db


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024))
    content = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.datetime.now)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))


db.create_all()
