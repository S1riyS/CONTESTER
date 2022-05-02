from flask import url_for, request

from app import db
from app.models import Grade, Topic, Task


def view_grade_dlc(*args, **kwargs):
    grade_number = request.view_args['grade_number']

    url = url_for('grade_page', grade_number=grade_number)
    return [{'text': f'{grade_number} класс', 'url': url}]


def view_topic_dlc(*args, **kwargs):
    grade_number = request.view_args['grade_number']

    topic_translit_name = request.view_args['topic_translit_name']
    topic = db.session.query(Topic).filter(Topic.translit_name == topic_translit_name).first()

    url = url_for('topic_page', grade_number=grade_number, topic_translit_name=topic_translit_name)
    return [{'text': topic.name, 'url': url}]


def view_task_dlc(*args, **kwargs):
    task_translit_name = request.view_args['task_translit_name']
    task = db.session.query(Task).filter(Task.translit_name == task_translit_name).first()

    return [{'text': task.name, 'url': ''}]
