from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate

from config import config

# Initialization of app
app = Flask(__name__)
app.config.from_object(config.get(environ.get('FLASK_CONFIG') or 'default'))

db = SQLAlchemy(app)
migrate = Migrate(app, db) # TODO: Пофиксить Flask-Migrate
# login_manager = LoginManager(app)
# moment = Moment(app)


# Jinja2 global variables
variables = {
    'WEBSITE_URL': 'contester.school17.perm.ru',
    'LANGUAGE': 'ru',
    'DEVELOPER': 'S1riyS'
}
for key, value in variables.items():
    app.jinja_env.globals[key] = value

db.init_app(app)

# Import routes
with app.app_context():
    from app import routes

    db.create_all()

    from app.models import init_db_data

    init_db_data()
