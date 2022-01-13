from flask import Blueprint, render_template

errors = Blueprint('errors', __name__, template_folder='templates', static_folder='static')

errors_data = {
    403: {
        'error_number': 403,
        'error_text': 'У вас не доступа к этой странице'
    },
    404: {
        'error_number': 404,
        'error_text': 'Данной страницы не существует'
    },
    500: {
        'error_number': 500,
        'error_text': 'Внутренняя ошибка сервера'
    }
}


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/error.html', data=errors_data[403]), 403


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/error.html', data=errors_data[404]), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/error.html', data=errors_data[500]), 500
