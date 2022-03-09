from flask import Blueprint, render_template

from app import db
from app.models import Grade, Topic


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
