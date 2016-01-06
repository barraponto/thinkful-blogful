import os
import unittest

os.environ['CONFIG_PATH'] = 'blogful.config.TestingConfig'

from blogful.app import app
from blogful.forms import EntryForm


class EntryFormTests(unittest.TestCase):
    def test_title_required(self):
        formdata = {'content': 'some text'}
        with app.test_request_context(method='POST', data=formdata):
            form = EntryForm()
            self.assertFalse(form.validate())
    def test_content_required(self):
        formdata = {'title': 'some title'}
        with app.test_request_context(method='POST', data=formdata):
            form = EntryForm()
            self.assertFalse(form.validate())
    def test_data_acceptable(self):
        formdata = {'title': 'some title', 'content': 'some text'}
        with app.test_request_context(method='POST', data=formdata):
            form = EntryForm()
            self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()
