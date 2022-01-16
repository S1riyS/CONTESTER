from flask import render_template, url_for

from . import app
from app.blueprints.admin.admin import admin
from app.blueprints.api.api import api
from app.blueprints.errors.handler import errors

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


@app.route('/<int:grade>', methods=['GET'])
def grade_page(grade):
    return render_template('grade.html', grade=grade)


@app.route('/<int:grade>/<string:topic>', methods=['GET'])
def topic_page(grade, topic):
    return render_template('topic.html', grade=grade, topic=topic)


@app.route('/<int:grade>/<string:topic>/<int:task_number>', methods=['GET'])
def task_page(grade, topic, task_number):
    breadcrumbs_args = ({'text': f'{grade} класс', 'link': url_for('grade_page', grade=grade)},
                        {'text': topic, 'link': url_for('topic_page', grade=grade, topic=topic)},
                        {'text': f'Task №{task_number}', 'link': None})

    breadcrumbs_html = render_template('breadcrumbs.html', breadcrumbs=breadcrumbs_args)

    return render_template('task.html', grade=grade, topic=topic, task_number=task_number,
                           languages=languages, breadcrumbs=breadcrumbs_html)
