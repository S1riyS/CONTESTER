from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
default_breadcrumb_root(admin, '.')

from app.blueprints.admin import routes