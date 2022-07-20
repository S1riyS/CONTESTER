from flask import Blueprint, render_template

from app import db
from app.models import Grade, Topic
from .forms import TopicForm, TaskForm

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


# Admin
@admin.route('/')
def home_page():
    return render_template('admin/admin.html', title='Админ панель')


@admin.route('/task/create', methods=['GET', 'POST'])
def create_task_page():
    # Tuple of grades
    grades = db.session.query(Grade).all()
    grades_tuple = [(grade.id, grade.number) for grade in grades]
    # Tuple of topics
    topics = db.session.query(Topic).filter_by(grade_id=1).all()
    topics_tuple = [(topic.id, topic.name) for topic in topics]
    # Initializing form
    form = TaskForm()
    form.grade.choices = grades_tuple
    form.topic.choices = topics_tuple

    return render_template('admin/task.html', title='Создать задачу', form=form)


@admin.route('/task/edit', methods=['GET', 'POST'])
def edit_task_page():
    ...


@admin.route('/topic/create', methods=['GET', 'POST'])
def create_topic_page():
    grades = db.session.query(Grade).all()
    grades_list = [(grade.id, grade.number) for grade in grades]

    form = TopicForm()
    form.grade.choices = grades_list

    return render_template('admin/topic.html', title='Создать тему', form=form)


@admin.route('/topic/edit', methods=['GET', 'POST'])
def edit_topic_page():
    ...
