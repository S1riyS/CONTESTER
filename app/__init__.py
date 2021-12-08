from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_moment import Moment
from flask_migrate import Migrate

from config import Config

# Initialization of app
app = Flask(__name__)
app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
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

# Import routes
with app.app_context():
    from . import routes
