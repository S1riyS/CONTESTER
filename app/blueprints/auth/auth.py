from flask import Blueprint, render_template, redirect, url_for, make_response, jsonify
from flask_login import current_user
from itsdangerous import SignatureExpired, BadSignature

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
    if not current_user.verified:
        try:
            email = serializer.loads(token, salt='confirm-email', max_age=3600)

        except BadSignature:
            return render_template('auth/after_confirm.html',
                                   title='Подтверждение почты',
                                   status='Несуществующий токен подтверждения!',
                                   success=False)

        except SignatureExpired:
            return render_template('auth/after_confirm.html',
                                   title='Подтверждение почты',
                                   status='Время подтверждения истекло',
                                   success=False)

        return render_template('auth/after_confirm.html',
                               title='Подтверждение почты',
                               status='Ваша почта подтверждена!',
                               success=True)

    return redirect(url_for('home_page'))
