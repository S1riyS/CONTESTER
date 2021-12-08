from flask import Blueprint, render_template, request, jsonify

from app.contester.contester import Contester

api = Blueprint('api', __name__)
contester = Contester()


# API
@api.route('/send_code', methods=['POST'])
def send_code():
    data = request.json

    tests = contester.get_tests({})
    response = contester.run_tests(code_value=data['code'], language=data['lang'], tests=tests)

    return jsonify('', render_template('code_response_model.html', response=response))
