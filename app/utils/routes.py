from functools import wraps
from flask import session, request


# Decoration function which adds current url to session variable
def next_url(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        session['next_url'] = request.url
        return func(*args, **kwargs)

    return wrapper_function
