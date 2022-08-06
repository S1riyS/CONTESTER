from flask import render_template, make_response
from werkzeug.exceptions import HTTPException

from app.blueprints.errors import errors

ERRORS_DATA = {
    403: {
        'description': 'У вас не доступа к этой странице'
    },
    404: {
        'description': 'Данной страницы не существует'
    },
    500: {
        'description': 'Внутренняя ошибка сервера'
    }
}

DEFAULT_ERRORS_DATA = {
    'description': 'Что-то пошло не так'
}


@errors.app_errorhandler(HTTPException)
def handle_exception(e):
    data = ERRORS_DATA.get(e.code, DEFAULT_ERRORS_DATA)
    return make_response(render_template('errors/error.html', code=e.code, data=data), e.code)
