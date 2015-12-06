import os

import requests
from flask.ext.script import Manager

from blogful import app
from blogful.database import db
from blogful.models import Entry

manager = Manager(app)

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

if __name__ == '__main__':
    manager.run()
