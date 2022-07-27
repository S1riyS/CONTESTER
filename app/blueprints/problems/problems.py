from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import current_user, login_required
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb

from app import db
from app.models import Grade, Topic
from app.contester.languages import languages
from app.utils.routes import grade_compliance_required
from app.utils.db import get_task
import app.breadcrumbs as bc

problems = Blueprint('problems', __name__, template_folder='templates', static_folder='static')
default_breadcrumb_root(problems, '.')


@problems.route('/redirect', methods=['GET'])
@login_required
def redirect_page():
    if current_user.is_admin:
        return redirect(url_for('problems.all_grades_page'))
    return redirect(url_for('problems.grade_page', grade_number=current_user.grade.number))


@problems.route('/', methods=['GET'])
@login_required
def all_grades_page():
    if current_user.is_admin:
        return render_template('problems/all_grades.html', title='Все классы', grades=db.session.query(Grade).all())
    abort(403)


@problems.route('/grade-<int:grade_number>', methods=['GET'])
@register_breadcrumb(problems, '.grade', '', dynamic_list_constructor=bc.view_grade_dlc)
@login_required
@grade_compliance_required
def grade_page(grade_number):
    grade = db.session.query(Grade).filter(Grade.number == grade_number).first_or_404()
    topics = grade.topics.all()

    context = {
        'grade': grade,
        'topics': topics,
    }

    return render_template('problems/grade.html', title=f'{grade.number} класс', **context)


@problems.route('/grade-<int:grade_number>/<string:topic_translit_name>', methods=['GET'])
@register_breadcrumb(problems, '.grade.topic', '', dynamic_list_constructor=bc.view_topic_dlc)
@login_required
@grade_compliance_required
def topic_page(grade_number, topic_translit_name):
    grade = db.session.query(Grade).filter(Grade.number == grade_number).first_or_404()
    topic = db.session.query(Topic).filter(Topic.translit_name == topic_translit_name).first_or_404()
    tasks = topic.tasks.all()

    context = {
        'grade': grade,
        'topic': topic,
        'tasks': tasks
    }
    return render_template('problems/topic.html', title=topic.name, **context)


@problems.route('/grade-<int:grade_number>/<string:topic_translit_name>/<string:task_translit_name>', methods=['GET'])
@register_breadcrumb(problems, '.grade.topic.task', '', dynamic_list_constructor=bc.view_task_dlc)
@login_required
@grade_compliance_required
def task_page(grade_number, topic_translit_name, task_translit_name):
    task = get_task(grade_number, topic_translit_name, task_translit_name)
    topic = task.topic
    grade = topic.grade

    context = {
        'task': task,
        'topic': topic,
        'grade': grade,
        'language_dict': languages.dictionary
    }

    return render_template('problems/task.html', title=task.name, **context)
