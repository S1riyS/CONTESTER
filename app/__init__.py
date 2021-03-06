from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail
from flask_breadcrumbs import Breadcrumbs
from itsdangerous import URLSafeTimedSerializer

from config import config

# Initialization of app
app = Flask(__name__)
app.config.from_object(config.get(environ.get('FLASK_CONFIG') or 'default'))

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login_manager = LoginManager(app)
moment = Moment(app)
breadcrumbs = Breadcrumbs(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY'))


# Jinja2 global variables
variables = {
    'WEBSITE_URL': 'contester.school17.perm.ru',
    'LANGUAGE': 'ru',
    'DEVELOPER': 'S1riyS'
}
for key, value in variables.items():
    app.jinja_env.globals[key] = value

# Import routes
from app import routes

with app.app_context():
    db.create_all()
    from app.models import init_db_data
    init_db_data()
