from flask import Blueprint, render_template, session, request, jsonify, make_response, url_for
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from sqlalchemy import and_

from app import db, serializer
from app.contester.contester import Contester

from app.models import User, Role, Grade, Topic, Task, Example, Test
from app.utils.email import send_email

api = Blueprint('api', __name__)
contester = Contester()


# TODO: Переименоаить API (api/create/task и т.д.)
def send_alert(success: bool, message: str):
    return make_response(jsonify(
        {
            'success': success,
            'message': message
        }
    ), 200)


# API
@api.route('/task/solution', methods=['POST'])
def send_solution():
    if not current_user.is_authenticated:
        return jsonify({
            'result': render_template('responses/code_error.html',
                                      message='Для отправки решений необходимо войти в систему')
        })

    elif not current_user.verified:
        return jsonify({
            'result': render_template('responses/code_error.html',
                                      message='Для отправки решений необходимо подтвердить свою почту')
        })

    data = request.json

    task = db.session.query(Task).filter(
        and_(
            Grade.number == data['path']['grade'],
            Topic.translit_name == data['path']['topic'],
            Task.translit_name == data['path']['task']
        )
    ).first()

    tests = task.get_tests()
    response = contester.run_tests(code=data['code'], language=data['lang'], tests=tests)

    if response is not None:
        return jsonify({
            'result': render_template('responses/code_success.html', response=response)
        })
    else:
        return jsonify({
            'result': render_template('responses/code_error.html', message='Что-то пошло не так!')
        })


@api.route('/task/submissions', methods=['POST'])
def get_submissions():
    return jsonify(render_template('responses/submissions.html'))


@api.route('/task/report', methods=['POST'])
def send_report():
    data = request.json
    print(data)
    return jsonify({'status': 'OK'})


@api.route('/topics', methods=['POST'])
def get_topics():
    data = request.json
    grade = db.session.query(Grade).filter(Grade.id == data['grade_id']).first()
    topics = grade.get_topics()

    return jsonify(render_template('admin/dropdown/topic_list.html', topics=topics))


# Auth api
@api.route('/auth/sign-up', methods=['POST'])
def signup():
    data = request.json
    print(data)

    if db.session.query(User).filter(User.email == data['email']).first():
        return send_alert(False, 'Пользователь с этой почтой уже зарегестрирован!')

    if data['password'] != data['password_again']:
        return send_alert(False, 'Пароли не совпадают')

    user = User(
        name=data['firstname'],
        surname=data['lastname'],
        email=data['email'],
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
    print(data)

    user = db.session.query(User).filter(User.email == data['email']).first()
    # Error
    if not user:
        return send_alert(False, 'Неверная почта или пароль')
    # Success
    elif user.check_password(data['password']):
        login_user(user)
        next_url = session['next_url'] or url_for('home_page')
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
                   text_body=f'Ваша ссылка для подтверждения: {link}',
                   html_body=render_template('auth/confirm_email.html', link=link))

    except Exception:
        return send_alert(False, 'При отправке письма произошла ошибка')

    return send_alert(True, 'Письмо с подтверждением отправлено')


# Admin API
@api.route('/admin/topic', methods=['POST'])
def create_topic():
    data = request.json
    print(data)

    topic = Topic(
        grade_id=data['grade_id'],
        name=data['name']
    )
    topic.set_translit_name()

    if not db.session.query(Topic).filter(Topic.translit_name == topic.translit_name).first():
        db.session.add(topic)
        db.session.commit()

        return send_alert(True, 'Тема успешно создана!')
    else:
        return send_alert(False, 'Тема с таким именем уже существует')


@api.route('/admin/task', methods=['POST'])
def create_task():
    data = request.json

    # Task
    task = Task(
        topic_id=data['path']['topic_id'],
        name=data['information']['name'],
        text=data['information']['condition']
    )
    task.set_translit_name()

    topic = db.session.query(Topic).filter(Topic.id == data['path']['topic_id']).first()
    translit_names = [task_.translit_name for task_ in topic.get_tasks()]

    if task.translit_name in translit_names:
        return send_alert(False, 'Задача с таким именем уже существует')

    else:
        db.session.add(task)
        db.session.commit()

        # Example
        example = Example(
            task_id=task.id,
            example_input=data['example']['input'],
            example_output=data['example']['output']
        )
        db.session.add(example)

        # Tests
        tests = zip(data['tests']['inputs'], data['tests']['outputs'], data['tests']['is_hidden'])
        for test_input, test_output, is_hidden in tests:
            test = Test(
                task_id=task.id,
                test_input=test_input,
                test_output=test_output,
                is_hidden=is_hidden
            )
            db.session.add(test)

        db.session.commit()

    return send_alert(True, 'Задача успешно создана')


@api.route('/admin/task', methods=['DELETE'])
def delete_task():
    data = request.json
    return jsonify({'status': 'OK'})


@api.route('/admin/test_block', methods=['POST'])
def get_task_input_block():
    data = request.json
    print(data)
    return jsonify(render_template('responses/single_test_block.html', test_number=data['test_number']))
