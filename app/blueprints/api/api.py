from flask import Blueprint, render_template, session, request, jsonify, make_response, url_for
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from sqlalchemy import and_

from app import db, serializer, contester
from app.contester.contester import contester
from app.contester.languages import languages

from app.models import User, Role, Grade, Topic, Task, Example, Test, Submission, load_user
from app.utils.email import send_email
from app.utils.db import get_task

api = Blueprint('api', __name__)


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
            'result': render_template('responses/solution/failure.html',
                                      message='Для отправки решений необходимо войти в систему')
        })

    elif not current_user.verified:
        return jsonify({
            'result': render_template('responses/solution/failure.html',
                                      message='Для отправки решений необходимо подтвердить свою почту')
        })

    data = request.json
    # Task
    path = data['path']
    task = get_task(path['grade'], path['topic'], path['task'])
    # Partner
    partner = load_user(data['partner_id'])
    # Code
    user_code = data['code'].strip()

    # submissions = db.session.query(Submission).filter(
    #     Submission.user_id == current_user.id,
    #     Submission.task_id == task.id
    # )
    #
    # # Validating code
    # if user_code in [submission.source_code for submission in submissions]:
    #     return jsonify({
    #         'result': render_template('responses/solution/failure.html',
    #                                   message='Решение с таким же кодом уже было отправлено')
    #     })

    response = contester.run_tests(code=user_code, language=data['lang'], task=task, partner=partner)

    if response is not None:
        return jsonify({
            'result': render_template('responses/solution/success.html', response=response)
        })

    return jsonify({
        'result': render_template('responses/solution/failure.html', message='Что-то пошло не так!')
    })


@api.route('/task/submissions', methods=['POST'])
def get_submissions():
    if current_user.is_authenticated:
        data = request.json
        task_path = data['task_path']
        task = get_task(task_path['grade'], task_path['topic'], task_path['task'])

        submissions = []
        for submission in current_user.submissions:
            if submission.task_id == task.id:
                submissions.append(submission)
    else:
        submissions = None

    return jsonify(render_template('responses/submissions_table.html', submissions=submissions))


@api.route('/task/report', methods=['POST'])
def send_report():
    data = request.json
    print(data)
    return jsonify({'status': 'OK'})


@api.route('/topics', methods=['POST'])
def get_topics():
    data = request.json
    grade = db.session.query(Grade).filter(Grade.id == data['grade_id']).first()
    topics = grade.topics

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
        name=data['name'].strip()
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
        name=data['information']['name'].strip(),
        text=data['information']['condition'].strip()
    )
    task.set_translit_name()

    topic = db.session.query(Topic).filter(Topic.id == data['path']['topic_id']).first()
    translit_names = [task_.translit_name for task_ in topic.tasks]

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
        tests = data['tests']
        tests_zip = zip(tests['inputs'], tests['outputs'], tests['is_hidden'])
        for test_input, test_output, is_hidden in tests_zip:
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
    return jsonify(render_template('responses/admin/single_test_block.html', test_number=data['test_number']))
