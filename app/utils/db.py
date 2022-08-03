import typing as t
from flask import url_for

from app import app, db
from app.models import Grade, Topic, Task


def get_task(grade_number, topic_translit_name, task_translit_name):
    return db.session.query(Task).filter(
        Grade.number == grade_number,
        Topic.translit_name == topic_translit_name,
        Task.translit_name == task_translit_name
    ).first_or_404()


def get_task_url(task: Task, tab: t.Optional[str] = None):
    topic = task.topic
    grade = topic.grade
    arguments = {
        'task_translit_name': task.translit_name,
        'topic_translit_name': topic.translit_name,
        'grade_number': grade.number,
        'tab': tab
    }
    return url_for('problems.task_page', **arguments)


app.jinja_env.globals.update(get_task_url=get_task_url)
