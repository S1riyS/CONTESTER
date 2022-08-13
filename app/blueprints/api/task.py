"""
Module with Task APIs
"""

from flask import request, make_response, jsonify, render_template
from flask_login import current_user

from app import db
from app.contester import contester, ContesterResponse
from app.models import Report, load_user
from app.blueprints.api import api
from app.utils.db import get_task
from .utils import send_alert


def render_solution_failure(message: str):
    return make_response(jsonify({
        'status': 'FAILED',
        'result': render_template(
            'responses/solution/failure.html',
            message=message
        )
    }), 200)


def render_solution_success(response: ContesterResponse):
    return make_response(jsonify({
        'status': 'OK',
        'result': render_template(
            'responses/solution/success.html',
            response=response
        )
    }), 200)


@api.route('/task/solution', methods=['POST'])
def send_solution():
    # Checking if user is authenticated
    if not current_user.is_authenticated:
        return render_solution_failure('Для отправки решений необходимо войти в систему')

    data = request.json

    # Checking if user's or partners profile is verified
    partner = load_user(data['partner_id'])  # Partner
    if not current_user.verified:
        return render_solution_failure('Для отправки решений вам необходимо подтвердить свою почту')
    if partner:
        if not partner.verified:
            return render_solution_failure('Для отправки решений вашему партнеру необходимо подтвердить свою почту')

    path = data['path']
    task = get_task(path['grade'], path['topic'], path['task'])  # Task
    code = data['code'].strip()  # Code

    response = contester.run_tests(
        code=code,
        language=data['lang'],
        task=task,
        partner=partner
    )

    if response is not None:
        return render_solution_success(response)

    return render_solution_failure('Что-то пошло не так!')


@api.route('/task/report', methods=['POST'])
def send_report():
    data = request.json
    try:
        path = data['path']
        task = get_task(path['grade'], path['topic'], path['task'])

        report = Report(
            user_id=current_user.id,
            task_id=task.id,
            text=data['text']
        )
        db.session.add(report)
        db.session.commit()

        return send_alert(True, 'Жалоба успешно отправлена')

    except Exception:
        return send_alert(False, 'Не удалось отправить жалобу')


@api.route('/task/report', methods=['DELETE'])
def delete_report():
    data = request.json
    try:
        report = db.session.query(Report).get(data['report_id'])
        db.session.delete(report)
        db.session.commit()

        return send_alert(True, 'Проблема отмечена как решенная')

    except Exception:
        return send_alert(False, 'Не удалось выполнить действие')
