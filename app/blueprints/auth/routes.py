from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from itsdangerous import SignatureExpired, BadSignature

from app import db, serializer
from app.blueprints.auth import auth
from app.models import Grade
from .forms import LoginForm, SignUpForm


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('auth/login.html', title='Вход', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup_page():
    grades = db.session.query(Grade).all()
    grades_list = [(grade.id, grade.number) for grade in grades]

    form = SignUpForm()
    form.grade.choices = grades_list
    return render_template('auth/sign_up.html', title='Регистрация', form=form)


@auth.route('/confirm-email/<string:token>')
@login_required
def confirm_email(token):
    if not current_user.verified:
        try:
            serializer.loads(token, salt='confirm-email', max_age=3600)
            current_user.verified = True
            db.session.commit()

        except SignatureExpired:
            return render_template(
                'auth/after_confirm.html',
                title='Подтверждение почты',
                status='Время подтверждения истекло',
                success=False
            )

        except BadSignature:
            return render_template(
                'auth/after_confirm.html',
                title='Подтверждение почты',
                status='Несуществующий токен подтверждения!',
                success=False
            )

        return render_template(
            'auth/after_confirm.html',
            title='Подтверждение почты',
            status='Ваша почта подтверждена!',
            success=True
        )

    return redirect(url_for('home_page'))
