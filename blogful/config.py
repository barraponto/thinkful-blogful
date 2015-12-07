class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/tf-blogful'
    DEBUG = True
    SECRET_KEY = 'this-is-just-for-development'
