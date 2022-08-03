from flask import Blueprint, render_template, session, request, jsonify, make_response, url_for
from flask_login import login_user, logout_user, current_user
from sqlalchemy import and_

from app import db, serializer, contester
from app.contester import contester

from app.models import User, Role, Grade, Topic, Task, Example, Test, Report, load_user
from app.utils.email import send_email
from app.utils.db import get_task

api = Blueprint('api', __name__)


def send_alert(success: bool, message: str):
    return make_response(jsonify(
        {
            'success': success,
            'message': message
        }
    ), 200)


def render_solution_failure(message: str):
    return make_response(jsonify({
        'result': render_template(
            'responses/solution/failure.html',
            message=message
        )
    }), 200)


def tests_to_orm_objects(tests, task):
    """Saves tests to database and returns list of ORM Test objects"""
    tests_zip = zip(tests['stdin_list'], tests['stdout_list'], tests['is_hidden_list'])
    tests_list = []
    for stdin, stdout, is_hidden in tests_zip:
        test = Test(
            task_id=task.id,
            stdin=stdin,
            stdout=stdout,
            is_hidden=is_hidden
        )
        tests_list.append(test)
        db.session.add(test)

    db.session.commit()

    return tests_list


# API
@api.route('/task/solution', methods=['POST'])
def send_solution():
    # Checking if user is authenticated
    if not current_user.is_authenticated:
        return render_solution_failure('Для отправки решений необходимо войти в систему')

    data = request.json
    path = data['path']
    task = get_task(path['grade'], path['topic'], path['task'])  # Task

    partner = load_user(data['partner_id'])  # Partner

    # Checking if user's or partners profile is verified
    if not current_user.verified:
        return render_solution_failure('Для отправки решений вам необходимо подтвердить свою почту')
    if partner:
        if not partner.verified:
            return render_solution_failure('Для отправки решений вашему партнеру необходимо подтвердить свою почту')

    code = data['code'].strip()  # Code

    response = contester.run_tests(
        code=code,
        language=data['lang'],
        task=task,
        partner=partner
    )

    if response is not None:
        return make_response(jsonify({
            'result': render_template(
                'responses/solution/success.html',
                response=response
            )
        }), 200)

    return render_solution_failure('Что-то пошло не так!')


@api.route('/task/report', methods=['POST'])
def send_report():
    data = request.json
    try:
        path = data['path']
        task = get_task(path['grade'], path['topic'], path['task'])

        report = Report(
            user_id=current_user.id,
            task_id=task.id,
            text=data['text']
        )
        db.session.add(report)
        db.session.commit()

        return send_alert(True, 'Жалоба успешно отправлена')

    except Exception:
        return send_alert(False, 'Не удалось отправить жалобу')


@api.route('/task/report', methods=['DELETE'])
def delete_report():
    data = request.json
    try:
        report = db.session.query(Report).get(data['report_id'])
        db.session.delete(report)
        db.session.commit()

        return send_alert(True, 'Проблема отмечена как решенная')

    except Exception:
        return send_alert(False, 'Не удалось выполнить действие')


@api.route('/topics', methods=['POST'])
def get_topics():
    data = request.json
    grade = db.session.query(Grade).filter(Grade.id == data['grade_id']).first()

    topics_array = []
    for topic in grade.topics:
        topics_array.append({
            'id': topic.id,
            'name': topic.name
        })

    return jsonify({'topics': topics_array})


# Auth api
@api.route('/auth/sign-up', methods=['POST'])
def signup():
    data = request.json
    print(data)

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
    print(data)

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


# Admin API
@api.route('/admin/topic', methods=['POST'])
def create_topic():
    data = request.json
    print(data)

    topic = Topic(
        grade_id=data['grade_id'],
        name=data['name'].strip()
    )
    topic.set_translit_name()

    if not db.session.query(Topic).filter(Topic.translit_name == topic.translit_name).first():
        db.session.add(topic)
        db.session.commit()

        return send_alert(True, 'Тема успешно создана!')
    else:
        return send_alert(False, 'Тема с таким именем уже существует')


@api.route('/admin/topic/<topic_id>', methods=['PUT'])
def update_topic(topic_id):
    data = request.json

    try:
        topic = db.session.query(Topic).get(topic_id)

        # Updating general info
        topic.grade_id = data['grade_id']
        topic.name = data['name']
        db.session.commit()

        return send_alert(True, 'Тема успешно обновлена!')

    except Exception:
        return send_alert(False, 'Не удалось обновить тему')


@api.route('/admin/task', methods=['POST'])
def create_task():
    data = request.json
    print(data)

    # Task
    task = Task(
        topic_id=data['path']['topic_id'],
        name=data['info']['name'].strip(),
        text=data['info']['condition'].strip()
    )
    task.set_translit_name()

    # Checking whether a task with this name already exists
    topic = db.session.query(Topic).get(data['path']['topic_id'])
    translit_names = [task_.translit_name for task_ in topic.tasks]
    if task.translit_name in translit_names:
        return send_alert(False, 'Задача с таким именем уже существует')

    else:
        db.session.add(task)
        db.session.commit()

        # Example
        example = Example(
            task_id=task.id,
            example_input=data['example']['stdin'],
            example_output=data['example']['stdout']
        )
        db.session.add(example)

        # Tests
        tests_to_orm_objects(data['tests'], task)

    return send_alert(True, 'Задача успешно создана')


@api.route('/admin/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    try:
        task = db.session.query(Task).get(task_id)

        # Updating general info
        task.topic_id = data['path']['topic_id']
        task.name = data['info']['name'].strip()
        task.text = data['info']['condition'].strip()
        task.set_translit_name()

        # Updating example
        task.example.example_input = data['example']['stdin']
        task.example.example_output = data['example']['stdout']

        # Deleting old tests
        for test in task.tests:
            db.session.delete(test)
        db.session.commit()

        # Adding new tests
        for test in tests_to_orm_objects(data['tests'], task):
            task.tests.append(test)
        db.session.commit()

        return send_alert(True, 'Задача успешно обновлена')

    except Exception:
        return send_alert(False, 'Не удалось обновить задачу')


@api.route('/admin/task', methods=['DELETE'])
def delete_task():
    data = request.json

    task = db.session.query(Task).get(data['task_id'])
    topic_url = url_for(
        'problems.topic_page',
        grade_number=task.topic.grade.number,
        topic_translit_name=task.topic.translit_name
    )

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'success': True, 'redirect_url': topic_url}), 200)
