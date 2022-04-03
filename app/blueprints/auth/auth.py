from flask import Blueprint, render_template, make_response, jsonify
from itsdangerous import SignatureExpired

from app import db, serializer
from app.models import User, Role
from app.forms.auth import LoginForm, SignUpForm


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('auth/login.html', title='Вход', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = SignUpForm()
    return render_template('auth/sign_up.html', title='Регистрация', form=form)

@auth.route('/confirm-email/<string:token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='confirm-email', max_age=3600)


    except SignatureExpired:
        return '<h1>The token is expired</h1>'

    return '<h1>The token works</h1>'