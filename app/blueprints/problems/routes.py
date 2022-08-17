from flask import current_app as app
from flask import render_template, redirect, url_for, request, abort
from flask_login import current_user, login_required
from flask_breadcrumbs import register_breadcrumb
from sqlalchemy import desc

from app import db
from app.blueprints.problems import problems
from app.models import Grade, Topic, Submission
from app.contester.languages import languages
from app.utils.routes import grade_compliance_required, admin_required
from app.utils.db import get_task
import app.utils.breadcrumbs as bc


@problems.route('/redirect', methods=['GET'])
@login_required
def redirect_page():
    if current_user.is_admin:
        return redirect(url_for('problems.all_grades_page'))
    return redirect(url_for('problems.grade_page', grade_number=current_user.grade.number))


@problems.route('/', methods=['GET'])
@login_required
@admin_required
def all_grades_page():
    return render_template('problems/all_grades.html', title='Все классы', grades=db.session.query(Grade).all())


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
    print(tasks)

    context = {
        'grade': grade,
        'topic': topic,
        'tasks': tasks
    }
    return render_template('problems/topic.html', title=topic.name, **context)


@problems.route(
    '/grade-<int:grade_number>/<string:topic_translit_name>/<string:task_translit_name>',
    defaults={'tab': 'problem'},
    methods=['GET']
)
@problems.route(
    '/grade-<int:grade_number>/<string:topic_translit_name>/<string:task_translit_name>/<string:tab>',
    methods=['GET']
)
@register_breadcrumb(problems, '.grade.topic.task', '', dynamic_list_constructor=bc.view_task_dlc)
@login_required
@grade_compliance_required
def task_page(grade_number, topic_translit_name, task_translit_name, tab):
    task = get_task(grade_number, topic_translit_name, task_translit_name)
    topic = task.topic

    global_context = {
        'task': task,
        'topic': topic,
    }

    page = request.args.get('table_page', type=int, default=1)

    if tab == 'problem':
        # Tab with problem (name, condition, editor etc)
        local_context = {
            'language_dict': languages.dictionary
        }
        return render_template(
            'problems/tabs/problem.html',
            title=f'{task.name} - Задача',
            **global_context,
            **local_context
        )

    elif tab == 'submissions':
        # Tab with user's submissions
        local_context = {
            'submissions': current_user.submissions.filter(
                Submission.task_id == task.id
            ).paginate(
                per_page=app.config['RECORDS_PER_PAGE'], page=page, error_out=False
            )
        }
        return render_template(
            'problems/tabs/submissions.html',
            title=f'{task.name} - Мои отправки',
            **global_context,
            **local_context
        )

    elif tab == 'all-submissions':
        # Tab with all submissions
        if current_user.is_admin:
            local_context = {
                'submissions': task.submissions.order_by(
                    desc(Submission.submission_date)
                ).paginate(
                    per_page=app.config['RECORDS_PER_PAGE'], page=page, error_out=False
                ),
                'show_users': True
            }
            return render_template(
                'problems/tabs/all_submissions.html',
                title=f'{task.name} - Все отправки',
                **global_context,
                **local_context
            )

        abort(403)

    abort(404)
