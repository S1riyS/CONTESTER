from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root

problems = Blueprint('problems', __name__, template_folder='templates', static_folder='static')
default_breadcrumb_root(problems, '.')

from app.blueprints.problems import routes