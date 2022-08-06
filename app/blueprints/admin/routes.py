from enum import Enum
from datetime import date

from sqlalchemy import asc, desc, func, not_
from flask import current_app as app
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user
from flask_breadcrumbs import register_breadcrumb

from app import db
from app.blueprints.admin import admin
from app.models import User, Topic, Task, Submission, Report
from app.utils.forms import init_grades_select, init_topics_select

from .forms import TopicForm, TaskForm


class ActionType(str, Enum):
    CREATE = 'create'
    EDIT = 'edit'


@admin.before_request
def admin_role_required():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login_page'))
    if not current_user.is_admin:
        abort(403)


@admin.add_app_template_global
def check_for_reports():
    if db.session.query(Report).first():
        return True
    return False


@admin.route('/')
@register_breadcrumb(admin, '.admin', 'Админ панель')
def home_page():
    page = request.args.get('table_page', type=int, default=1)
    submission_table = {
        'submissions': (
            db.session.query(Submission).filter(
                func.date(Submission.submission_date) == date.today()
            ).order_by(
                desc(Submission.submission_date)
            ).paginate(
                per_page=app.config['RECORDS_PER_PAGE'], page=page, error_out=False
            )
        ),
        'show_task': True,
        'show_users': True
    }
    return render_template('admin/admin.html', title='Админ панель', **submission_table)


@admin.route('/students', methods=['GET', 'POST'])
def students_page():
    number = request.args.get('number')
    letter = request.args.get('letter')

    users = db.session.query(User).filter(
        User.grade.has(number=number),
        User.grade_letter == letter
    ).order_by(
        asc(User.surname)
    ).all()

    table_data = []
    for user in users:
        solved_today = db.session.query(Submission).filter(
            func.date(Submission.submission_date) == date.today(),
            not_(Submission.test_results.any(success=False)),
            Submission.users.any(id=user.id)
        ).count()

        table_data.append({
            'user': user,
            'solved_today': solved_today
        })

    return render_template('admin/students.html', title=f'Ученики {number}{letter} класса', table_data=table_data)


@admin.route('/task/create', methods=['GET', 'POST'])
@register_breadcrumb(admin, '.admin.create_task', 'Создание задачи')
def create_task_page():
    form = TaskForm()
    init_grades_select(form=form)
    init_topics_select(form=form)

    return render_template('admin/task.html', title='Создать задачу', form=form, action=ActionType.CREATE)


@admin.route('/task/edit', methods=['GET', 'POST'])
@register_breadcrumb(admin, '.admin.edit_task', 'Редактирование задачи')
def edit_task_page():
    task_id = request.args.get('id')
    task = db.session.query(Task).get_or_404(task_id)

    form = TaskForm(
        obj=task,
        grade_id=task.topic.grade_id,
        condition=task.text,
        example_stdin=task.example.example_input,
        example_stdout=task.example.example_output
    )
    init_grades_select(form=form)
    init_topics_select(form=form, grade_id=task.topic.grade_id)

    return render_template('admin/task.html', title='Редактировать задачу', form=form, action=ActionType.EDIT)


@admin.route('/topic/create', methods=['GET', 'POST'])
@register_breadcrumb(admin, '.admin.create_topic', 'Создание темы')
def create_topic_page():
    form = TopicForm()
    init_grades_select(form=form)

    return render_template('admin/topic.html', title='Создать тему', form=form, action=ActionType.CREATE)


@admin.route('/topic/edit', methods=['GET', 'POST'])
@register_breadcrumb(admin, '.admin.edit_topic', 'Редактирование темы')
def edit_topic_page():
    topic_id = request.args.get('id')
    topic = db.session.query(Topic).get_or_404(topic_id)

    form = TopicForm(obj=topic)
    init_grades_select(form=form)

    return render_template('admin/topic.html', title='Редактировать тему', form=form, action=ActionType.EDIT)


@admin.route('/reports', methods=['GET', 'POST'])
@register_breadcrumb(admin, '.admin.reports', 'Жалобы')
def reports_page():
    reports = db.session.query(Report).all()
    return render_template('admin/reports.html', title='Жалобы', reports=reports)
