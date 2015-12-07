import os
import random
import string

import requests
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash

from blogful import app
from blogful.database import db
from blogful.models import Entry, User


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@manager.command
def seed(entries=10):
    response = requests.get(
        'http://loripsum.net/api/{}/medium/plaintext'.format(entries))
    lorem_generator = filter(None, response.text.splitlines())
    for index, lorem in enumerate(lorem_generator, start=1):
        db.session.add(Entry(
            title='Test Entry #{}'.format(index),
            content=lorem
        ))
    db.session.commit()

@manager.command
def adduser():
    name = input('Name: ')
    email = input('Email: ')
    password = ''.join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(32))

    if User.query.filter_by(email=email).first():
        raise ValueError('User with that email already exists.')

    db.session.add(User(name=name, email=email,
                        password=generate_password_hash(password)))
    db.session.commit()

    print('Created user {} with password {!r}'.format(email, password))


if __name__ == '__main__':
    manager.run()
