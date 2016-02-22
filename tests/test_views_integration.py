import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

os.environ['CONFIG_PATH'] = 'blogful.config.TestingConfig'
from blogful import app
from blogful.database import db
from blogful.models import User, Entry


class FlaskViewTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        db.create_all()
        db.session.add_all(self.fixtures.values())
        db.session.commit()
        assert [db.session.refresh(fixture) for fixture in self.fixtures.values()]

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def simulate_login(self, user):
        with self.client.session_transaction() as http_session:
            http_session['user_id'] = str(user.id)
            http_session['_fresh'] = True


class TestAddEntry(FlaskViewTestCase):

    def setUp(self):
        self.fixtures = {
            'alice': User(name='Alice', email='alice@example.com',
                          password=generate_password_hash('alice'))}
        super(TestAddEntry, self).setUp()

    def test_add_entry(self):
        self.simulate_login(self.fixtures['alice'])
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
        self.assertEqual(entry.author, self.fixtures['alice'])


class TestEditEntry(FlaskViewTestCase):

    def setUp(self):
        self.fixtures = {
            'alice': User(name='Alice', email='alice@example.com',
                        password=generate_password_hash('alice')),
            'bob': User(name='Bob', email='bob@example.com',
                        password=generate_password_hash('bob'))}
        self.fixtures.update({
            'entry': Entry(title='Test Entry', content='Test Content',
                           author=self.fixtures['alice'])})
        super(TestEditEntry, self).setUp()

    def test_unauthorized_edit_entry(self):
        self.simulate_login(self.fixtures['bob'])
        response = self.client.post(
            '/entry/{}/edit'.format(self.fixtures['entry'].id),
            data={'content': 'New Test Content'})

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
