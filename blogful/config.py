class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/tf-blogful'
    DEBUG = True
    SECRET_KEY = 'this-is-just-for-development'


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/tf-blogful-tests'
    DEBUG = False
    SECRET_KEY = 'this-is-just-for-testing'
    WTF_CSRF_ENABLED = False


class TravisConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/tf-blogful-tests'
