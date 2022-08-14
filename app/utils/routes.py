from functools import wraps

from flask import session, request, abort
from flask_login import current_user


# Decorator function which adds current url to session variable
def next_url(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        session['next_url'] = request.url
        return func(*args, **kwargs)

    return wrapper_function


# Decorator that raises "Access Forbidden" error if user doesn't belong to the corresponding grade
def grade_compliance_required(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        if current_user.role_id != 2:
            if current_user.grade.number != kwargs.get('grade_number'):
                abort(403)
        return func(*args, **kwargs)

    return wrapper_function


# Admin role required
def admin_required(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        abort(403)

    return wrapper_function
