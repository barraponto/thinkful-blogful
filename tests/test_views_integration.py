import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

os.environ['CONFIG_PATH'] = 'blogful.config.TestingConfig'
from blogful import app
from blogful.database import db
from blogful.models import User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        db.create_all()
        self.user = User(name='Alice', email='alice@example.com',
                         password=generate_password_hash('test'))
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session['user_id'] = str(self.user.id)
            http_session['_fresh'] = True

    def test_add_entry(self):
        self.simulate_login()
        response = self.client.post('/entry/add', data={
            'title': 'Test Entry',
            'content': 'Test Content'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, '/')

        entries = Entry.query.all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertEqual(entry.title, 'Test Entry')
        self.assertEqual(entry.content, 'Test Content')
        self.assertEqual(entry.author, self.user)




if __name__ == '__main__':
    unittest.main()
