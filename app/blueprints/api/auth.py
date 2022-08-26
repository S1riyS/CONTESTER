"""
Module with Auth APIs
"""

from flask import request, session, make_response, jsonify, render_template, url_for
from flask_login import login_user, logout_user, current_user

from app import db, serializer
from app.models import User, Role
from app.blueprints.api import api
from app.utils.email import send_email
from .utils import send_alert


@api.route('/auth/sign-up', methods=['POST'])
def signup():
    data = request.json

    if db.session.query(User).filter(User.email == data['email']).first():
        return send_alert(False, 'Пользователь с этой почтой уже зарегистрирован!')

    if data['password'] != data['password_again']:
        return send_alert(False, 'Пароли не совпадают')

    user = User(
        name=data['firstname'].strip().capitalize(),
        surname=data['lastname'].strip().capitalize(),
        email=data['email'].strip(),
        role_id=db.session.query(Role).filter(Role.name == 'user').first().id,
        grade_id=data['grade'],
        grade_letter=data['letter'],
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    next_url = session['next_url'] or url_for('home_page')
    return make_response(jsonify({'success': True, 'redirect_url': next_url}), 200)


@api.route('/auth/login', methods=['POST'])
def login():
    data = request.json

    user = db.session.query(User).filter(User.email == data['email']).first()
    # Error
    if not user:
        return send_alert(False, 'Неверная почта или пароль')

    # Success
    elif user.check_password(data['password']):
        login_user(user)

        if 'next_url' in session:
            next_url = session['next_url']
        else:
            next_url = url_for('home_page')

        return make_response(jsonify({'success': True, 'redirect_url': next_url}), 200)

    # Error
    else:
        return send_alert(False, 'Неверная почта или пароль')


@api.route('/auth/logout', methods=['POST'])
def logout():
    logout_user()
    return make_response(jsonify({'redirect_url': url_for('home_page')}), 200)


@api.route('/auth/confirm-email', methods=['PUT'])
def confirm_email():
    try:
        email = current_user.email
        token = serializer.dumps(email, salt='confirm-email')
        link = url_for('auth.confirm_email', token=token, _external=True)
        print(email, token, link)

        send_email(subject='Подтвердите адрес электронной почты',
                   recipients=[email],
                   html_body=render_template('auth/confirm_email.html', link=link))

    except Exception:
        return send_alert(False, 'При отправке письма произошла ошибка')

    return send_alert(True, 'Письмо с подтверждением отправлено')
