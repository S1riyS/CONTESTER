from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root

problems = Blueprint('problems', __name__, template_folder='templates', static_folder='static', url_prefix='/problems')
default_breadcrumb_root(problems, '.')

from app.blueprints.problems import routes
