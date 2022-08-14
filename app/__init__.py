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

CONFIG = config.get(environ.get('FLASK_CONFIG') or 'default')

# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
breadcrumbs = Breadcrumbs()
mail = Mail()
serializer = URLSafeTimedSerializer(environ.get('SECRET_KEY', 'default_secret_key'))

# Jinja2 global variables
JINJA2_GLOBAL_VARIABLES = {
    'WEBSITE_URL': 'contester.school17.perm.ru',
    'LANGUAGE': 'ru',
    'DEVELOPER': 'S1riyS'
}


def create_app(config_class=CONFIG):
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    moment.init_app(app)
    breadcrumbs.init_app(app)
    mail.init_app(app)

    # Database initialization
    @app.before_request
    def init_db():
        db.create_all()
        from app.models import init_db_data
        init_db_data()

    with app.app_context():
        # Include routes
        from app import routes

        # Register blueprints
        from app.blueprints.auth import auth
        app.register_blueprint(auth)

        from app.blueprints.problems import problems
        app.register_blueprint(problems)

        from app.blueprints.admin import admin
        app.register_blueprint(admin)

        from app.blueprints.api import api
        app.register_blueprint(api)

        from app.blueprints.errors import errors
        app.register_blueprint(errors)

    # Jinja2 global variables
    for key, value in JINJA2_GLOBAL_VARIABLES.items():
        app.jinja_env.globals[key] = value

    return app
