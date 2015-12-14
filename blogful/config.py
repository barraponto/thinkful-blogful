class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/tf-blogful-tests'
    DEBUG = False
    SECRET_KEY = 'this-is-just-for-testing'

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/tf-blogful'
    DEBUG = True
    SECRET_KEY = 'this-is-just-for-development'
