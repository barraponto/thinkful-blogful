import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

os.environ['CONFIG_PATH'] = 'blogful.config.TestingConfig'
from blogful import app
from blogful.database import db
from blogful.models import User


class TestViews(unittest.TestCase):
    def setUp(self):
        # Setup client
        self.browser = Browser('phantomjs')

        # Setup DB
        db.create_all()
        # Create User
        self.user = User(name='Alice', email='alice@example.com',
                         password=generate_password_hash('test'))
        db.session.add(self.user)
        db.session.commit()

        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)

    def tearDown(self):
        self.process.terminate()
        db.session.close()
        db.drop_all()
        self.browser.quit()

    def test_login_correct(self):
        self.browser.visit('http://127.0.0.1:5000/login')
        self.browser.fill('email', 'alice@example.com')
        self.browser.fill('password', 'test')
        self.browser.find_by_css('button[type=submit]').click()
        self.assertEqual(self.browser.url, 'http://127.0.0.1:5000/')

if __name__ == '__main__':
    unittest.main()