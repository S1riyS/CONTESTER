from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__)) # Getting base directory
load_dotenv(path.join(basedir, '.env')) # Loading env

# Base Config
class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app', 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Developing Config
class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
