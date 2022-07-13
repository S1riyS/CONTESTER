from flask import render_template, redirect, url_for, request, session, abort
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb

from app import app, login_manager
from app.blueprints.admin.admin import admin
from app.blueprints.auth.auth import auth
from app.blueprints.api.api import api
from app.blueprints.errors.handler import errors
from app.blueprints.problems.problems import problems

from app.models import Submission
from app.contester.db_manager import load_from_database
from app.contester.languages import languages
from app.utils.routes import next_url

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(errors, url_prefix='/error')
app.register_blueprint(problems, url_prefix='/problems')


# Unauthorized handler
@login_manager.unauthorized_handler
def unauthorized_callback():
    session['next_url'] = request.path
    return redirect(url_for('auth.login_page'))


@app.route('/', methods=['GET'])
@register_breadcrumb(app, '.', 'Главная')
@next_url
def home_page():
    return render_template('new_home.html', title='Главная')


@app.route('/submissions/<int:submission_id>', methods=['GET'])
@login_required
def submission_page(submission_id):
    submission = Submission.query.get_or_404(submission_id)

    if submission in current_user.submissions:
        context = {
            'submission': submission,
            'language': languages.get_language(submission.language, object_only=True),
            'code': submission.processed_code,
            'response': load_from_database(submission)
        }
        return render_template('submission.html', title=f'Отправленное решение ({submission.task.name})', **context)

    abort(404)


@app.route('/profile', methods=['GET', 'POST'])
@register_breadcrumb(app, '.profile', 'Профиль')
@login_required
def profile_page():
    submission_table = {
        'submissions': current_user.submissions,
        'show_task': True
    }
    return render_template('profile.html', title='Профиль', **submission_table)
