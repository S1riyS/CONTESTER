from flask import render_template, url_for

from app import app, db
from app.blueprints.admin.admin import admin
from app.blueprints.api.api import api
from app.blueprints.errors.handler import errors

from app.models import Grade, Topic, Task, Example, Test

from app.contester.contester import languages

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(errors, url_prefix='/error')


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/all-tasks', methods=['GET'])
def lessons_page():
    return render_template('lessons.html')


@app.route('/<int:grade_number>', methods=['GET'])
def grade_page(grade_number):
    grade = db.session.query(Grade).filter(Grade.number == grade_number).first_or_404()
    topics = grade.get_topics()

    breadcrumbs = [
        {
            'text': f'{grade.number} класс',
            'link': None
        }
    ]

    return render_template('grade.html', grade=grade, topics=topics,
                           breadcrumbs=breadcrumbs)


@app.route('/<int:grade_number>/<string:topic_translit_name>', methods=['GET'])
def topic_page(grade_number, topic_translit_name):
    grade = db.session.query(Grade).filter(Grade.number == grade_number).first_or_404()
    topic = db.session.query(Topic).filter(Topic.translit_name == topic_translit_name).first_or_404()
    tasks = topic.get_tasks()

    breadcrumbs = [
        {
            'text': f'{grade.number} класс',
            'link': url_for('grade_page', grade_number=grade.number)
        },
        {
            'text': topic.name,
            'link': None
        },
    ]

    return render_template('topic.html', grade=grade, topic=topic, tasks=tasks,
                           breadcrumbs=breadcrumbs)


@app.route('/<int:grade_number>/<string:topic_translit_name>/<string:task_translit_name>', methods=['GET'])
def task_page(grade_number, topic_translit_name, task_translit_name):
    grade = db.session.query(Grade).filter(Grade.number == grade_number).first_or_404()
    topic = db.session.query(Topic).filter(Topic.translit_name == topic_translit_name).first_or_404()
    task = db.session.query(Task).filter(Task.translit_name == task_translit_name).first_or_404()

    breadcrumbs = [
        {
            'text': f'{grade.number} класс',
            'link': url_for('grade_page', grade_number=grade.number)
        },
        {
            'text': topic.name,
            'link': url_for('topic_page', grade_number=grade_number, topic_translit_name=topic_translit_name)
        },
        {
            'text': task.name,
            'link': None
        }
    ]


    return render_template('task.html', grade=grade, topic=topic, task=task,
                           languages=languages, breadcrumbs=breadcrumbs, is_admin=True)
