from flask import url_for, request
from flask_login import current_user

from app import db
from app.models import User, Topic, Task


def view_grade_dlc(*args, **kwargs):
    grade_number = request.view_args['grade_number']

    url = url_for('problems.grade_page', grade_number=grade_number)
    return [{'text': f'{grade_number} класс', 'url': url}]


def view_topic_dlc(*args, **kwargs):
    grade_number = request.view_args['grade_number']
    topic_translit_name = request.view_args['topic_translit_name']

    topic = db.session.query(Topic).filter(Topic.translit_name == topic_translit_name).first()
    if not topic:
        return [{'text': 'Тема не найдена', 'url': ''}]

    url = url_for('problems.topic_page', grade_number=grade_number, topic_translit_name=topic_translit_name)
    return [{'text': topic.name, 'url': url}]


def view_task_dlc(*args, **kwargs):
    task_translit_name = request.view_args['task_translit_name']
    task = db.session.query(Task).filter(Task.translit_name == task_translit_name).first()
    if not task:
        return [{'text': 'Задача не найдена', 'url': ''}]

    return [{'text': task.name, 'url': ''}]


def view_user_dlc(*args, **kwargs):
    user_id = request.view_args['user_id']
    if user_id is not None:
        user = db.session.query(User).get(user_id)
    else:
        user = current_user

    if not user:
        return [{'text': 'Пользователь не найден', 'url': ''}]

    return [{'text': f'{user.surname} {user.name}', 'url': ''}]
