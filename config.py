from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))  # Getting base directory
load_dotenv(path.join(basedir, '.env'))  # Loading env


# Base Config
class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app', 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    RECORDS_PER_PAGE = 10


# Production Config
class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


# Developing Config
class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}
