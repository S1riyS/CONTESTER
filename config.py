import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    SECRET_KEY = '1qaz2wsx3edc4rfv'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
