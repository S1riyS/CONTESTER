from flask import Blueprint, render_template

from app import db
from app.models import Grade, Topic

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# Admin
@admin.route('/')
def home_page():
    return render_template('admin/admin.html', title='Админ панель')

@admin.route('/task/create', methods=['GET', 'POST'])
def create_task_page():
    grades = db.session.query(Grade).all()
    topics = db.session.query(Topic).filter(Topic.grade_id == grades[0].id).all()

    rendered_topic_list = render_template('admin/dropdown/topic_list.html', topics=topics)
    rendered_grade_list = render_template('admin/dropdown/grade_list.html', grades=grades)

    return render_template('admin/create_task.html', title='Создать задачу',
                           rendered_grade_list=rendered_grade_list,
                           rendered_topic_list=rendered_topic_list)

@admin.route('/task/edit',  methods=['GET', 'POST'])
def edit_task_page():
    ...


@admin.route('/topic/create', methods=['GET', 'POST'])
def create_topic_page():
    grades = db.session.query(Grade).all()
    rendered_grade_list = render_template('admin/dropdown/grade_list.html', grades=grades)

    return render_template('admin/create_topic.html', title='Создать тему',
                           rendered_grade_list=rendered_grade_list)


@admin.route('/topic/edit',  methods=['GET', 'POST'])
def edit_topic_page():
    ...