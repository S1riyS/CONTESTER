from enum import Enum

from flask import Blueprint, render_template, request

from app import db
from app.models import Grade, Topic, Task
from app.utils.forms import init_grades_select, init_topics_select

from .forms import TopicForm, TaskForm


class ActionType(str, Enum):
    CREATE = 'create'
    EDIT = 'edit'


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


# Admin
@admin.route('/')
def home_page():
    return render_template('admin/admin.html', title='Админ панель', action=ActionType.CREATE)


@admin.route('/task/create', methods=['GET', 'POST'])
def create_task_page():
    form = TaskForm()
    init_grades_select(form=form)
    init_topics_select(form=form)

    return render_template('admin/task.html', title='Создать задачу', form=form, action=ActionType.CREATE)


@admin.route('/task/edit', methods=['GET', 'POST'])
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
def create_topic_page():
    form = TopicForm()
    init_grades_select(form=form)

    return render_template('admin/topic.html', title='Создать тему', form=form)


@admin.route('/topic/edit', methods=['GET', 'POST'])
def edit_topic_page():
    topic_id = request.args.get('id')
    topic = db.session.query(Topic).get_or_404(topic_id)

    form = TopicForm(obj=topic)
    init_grades_select(form=form)

    return render_template('admin/topic.html', title='Редактировать тему', form=form, action=ActionType.EDIT)
