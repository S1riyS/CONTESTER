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

    return render_template('grade.html', grade=grade, topics=topics)


@app.route('/<int:grade>/<string:topic>', methods=['GET'])
def topic_page(grade, topic):
    return render_template('topic.html', grade=grade, topic=topic)


@app.route('/<int:grade>/<string:topic>/<int:task_number>', methods=['GET'])
def task_page(grade, topic, task_number):
    breadcrumbs = ({'text': f'{grade} класс', 'link': url_for('grade_page', grade=grade)},
                   {'text': topic, 'link': url_for('topic_page', grade=grade, topic=topic)},
                   {'text': f'Task №{task_number}', 'link': None})

    return render_template('task.html', grade=grade, topic=topic, task_number=task_number,
                           languages=languages, breadcrumbs=breadcrumbs, is_admin=True)
