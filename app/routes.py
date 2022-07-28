from flask import render_template, redirect, url_for, request, session, abort
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb

from app import app, db, login_manager
from app.blueprints.admin.admin import admin
from app.blueprints.auth.auth import auth
from app.blueprints.api.api import api
from app.blueprints.errors.handler import errors
from app.blueprints.problems.problems import problems

from app.models import User, Submission
from app.contester.db_manager import load_from_database
from app.contester.languages import languages
from app.utils.routes import next_url
from app.utils.forms import init_grades_select
from app.forms.user import EditProfileForm
import app.breadcrumbs as bc

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

    if submission in current_user.submissions or current_user.is_admin:
        context = {
            'submission': submission,
            'language': languages.get_language(submission.language, object_only=True),
            'code': submission.processed_code,
            'response': load_from_database(submission)
        }
        return render_template('submission.html', title=f'Отправленное решение ({submission.task.name})', **context)

    abort(404)


@app.route('/profile', defaults={'user_id': None}, methods=['GET', 'POST'])
@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@register_breadcrumb(app, '.user', '', dynamic_list_constructor=bc.view_user_dlc)
@login_required
def profile_page(user_id):
    # User identification
    if user_id is not None:
        user: User = db.session.query(User).get_or_404(user_id)
        edit_permission = False

        # Redirecting to /profile if user_id from /user/<user_id> is current user's id
        if user.id == current_user.id:
            return redirect(url_for('profile_page', user_id=None))
    else:
        user: User = current_user
        edit_permission = True

    # Giving permission to edit user's profile if current user is admin
    if current_user.is_admin:
        edit_permission = True

    # Form initialization
    form = EditProfileForm(obj=user)
    init_grades_select(form)

    # Handling form submission
    if form.validate_on_submit():
        user.surname = form.surname.data.capitalize()
        user.name = form.name.data.capitalize()
        user.grade_id = form.grade_id.data
        user.grade_letter = form.grade_letter.data
        db.session.commit()

        return redirect(url_for('profile_page', user_id=user.id))

    # Forming table data
    table_data = {
        'submissions': user.submissions,
        'show_task': True
    }
    # Forming page context
    context = {
        'user': user,
        'form': form,
        'edit_permission': edit_permission,
    }

    return render_template('profile.html', title=f'{user.surname} {user.name}', **table_data, **context)
