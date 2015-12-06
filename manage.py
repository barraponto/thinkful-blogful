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
    for n in range(int(entries)):
        response = requests.get('http://loripsum.net/api/1/medium/plaintext')
        db.session.add(Entry(
            title='Test Entry #{}'.format(n),
            content=response.text.strip()
        ))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
