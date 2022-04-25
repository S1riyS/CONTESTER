from functools import wraps

from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_required

from app import app, db, login_manager
from app.blueprints.admin.admin import admin
from app.blueprints.auth.auth import auth
from app.blueprints.api.api import api
from app.blueprints.errors.handler import errors

from app.models import Grade, Topic, Task, Example, Test

from app.contester.contester import languages

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(errors, url_prefix='/error')


# Decoration function which adds current url to session variable
def next_url(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        session['next_url'] = request.url
        return func(*args, **kwargs)

    return wrapper_function


# Unauthorized handler
@login_manager.unauthorized_handler
def unauthorized_callback():
    session['next_url'] = request.path
    return redirect(url_for('auth.login_page'))


@app.route('/', methods=['GET'])
@next_url
def home_page():
    return render_template('home.html', title='Главная')


@app.route('/all-tasks', methods=['GET'])
@next_url
def lessons_page():
    return render_template('lessons.html', title='Все задания')


@app.route('/<int:grade_number>', methods=['GET'])
@next_url
def grade_page(grade_number):
    grade = db.session.query(Grade).filter(Grade.number == grade_number).first_or_404()
    topics = grade.get_topics()

    breadcrumbs = [
        {
            'text': f'{grade.number} класс',
            'link': None
        }
    ]

    return render_template('grade.html', title=f'{grade.number} класс',
                           grade=grade, topics=topics,
                           breadcrumbs=breadcrumbs)


@app.route('/<int:grade_number>/<string:topic_translit_name>', methods=['GET'])
@next_url
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

    return render_template('topic.html', title=topic.name,
                           grade=grade, topic=topic, tasks=tasks,
                           breadcrumbs=breadcrumbs)


@app.route('/<int:grade_number>/<string:topic_translit_name>/<string:task_translit_name>', methods=['GET'])
@next_url
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

    return render_template('task.html', title=task.name,
                           grade=grade, topic=topic, task=task, example=task.get_example(),
                           languages=languages, breadcrumbs=breadcrumbs,
                           is_admin=True)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    return render_template('profile.html', title='Профиль')
