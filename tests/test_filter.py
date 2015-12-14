import os
import unittest
import datetime

if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'blogful.config.TestingConfig'

import blogful
import blogful.filters

class FilterTests(unittest.TestCase):
    def test_date_format(self):
        date = datetime.date(1999, 12, 31)
        self.assertEqual(
            blogful.filters.dateformat(date, '%y/%m/%d'), '99/12/31')
    def test_date_format_none(self):
        self.assertEqual(
            blogful.filters.dateformat(None, '%y/%m/%d'), None)

if __name__ == '__main__':
    unittest.main()
