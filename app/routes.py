from flask import render_template

from . import app
from app.admin.admin import admin
from app.api.api import api
from app.errors.handler import errors

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
    return render_template('task.html', grade=grade, topic=topic, task_number=task_number, languages=languages)

