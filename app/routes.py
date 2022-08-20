from flask import current_app as app
from flask import render_template, redirect, url_for, request, session, abort
from flask_login import login_required, current_user
from flask_breadcrumbs import register_breadcrumb

from app import db, login_manager

from app.models import User, Role, Submission
from app.contester.db_manager import load_from_database
from app.contester.languages import languages
from app.utils.routes import next_url
from app.utils.forms import init_grades_select
from app.forms import EditProfileForm
import app.utils.breadcrumbs as bc


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


@app.route('/contacts', methods=['GET'])
@register_breadcrumb(app, '.contacts', 'Контакты')
@next_url
def contacts_page():
    return render_template('contacts.html', title='Контакты')


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
        # Redirecting to /profile if user_id from /user/<user_id> is current user's id
        if user.id == current_user.id:
            return redirect(url_for('profile_page', user_id=None))
        # Raising error 403 if not an admin tries to access someone else's profile
        elif not current_user.is_admin:
            abort(403)
    else:
        user: User = current_user

    # Form initialization
    form = EditProfileForm(obj=user)
    init_grades_select(form)

    # Handling form submission
    if form.validate_on_submit():
        # General info
        user.surname = form.surname.data.capitalize()
        user.name = form.name.data.capitalize()
        user.grade_id = form.grade_id.data
        user.grade_letter = form.grade_letter.data
        # Role
        if form.is_admin.data:
            role = db.session.query(Role).filter_by(name='admin').first()
        else:
            role = db.session.query(Role).filter_by(name='user').first()
        user.role_id = role.id

        db.session.commit()

        return redirect(url_for('profile_page', user_id=user.id))

    # Forming table data
    page = request.args.get('table_page', type=int, default=1)
    table_data = {
        'submissions': user.submissions.paginate(per_page=app.config['RECORDS_PER_PAGE'], page=page, error_out=False),
        'show_task': True,
    }
    # Forming page context
    context = {
        'user': user,
        'form': form,
    }

    return render_template('profile.html', title=f'{user.surname} {user.name}', **table_data, **context)
