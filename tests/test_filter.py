import os
import unittest
import datetime

if not 'CONFIG_PATH' in os.environ:
    os.environ['CONFIG_PATH'] = 'blog.config.TestingConfig'

import blog
import blog.filters

class FilterTests(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
