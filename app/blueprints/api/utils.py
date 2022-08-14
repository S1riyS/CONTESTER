"""
Module with API utils
"""

import typing as t

from flask import make_response, jsonify

from app import db
from app.models import Task, Test


def send_alert(success: bool, message: str):
    """Returns typed response than can be processes by sendDefaultAjax function in JS file"""
    return make_response(jsonify(
        {
            'success': success,
            'message': message
        }
    ), 200)


def tests_to_orm_objects(tests: dict, task: Task) -> t.Iterable[Test]:
    """Saves tests to database and returns list of ORM Test objects"""
    tests_zip = zip(tests['stdin_list'], tests['stdout_list'], tests['is_hidden_list'])
    tests_list = []
    for stdin, stdout, is_hidden in tests_zip:
        test = Test(
            task_id=task.id,
            stdin=stdin,
            stdout=stdout,
            is_hidden=is_hidden
        )
        tests_list.append(test)
        db.session.add(test)

    db.session.commit()

    return tests_list
