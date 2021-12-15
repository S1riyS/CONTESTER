from flask import Blueprint, render_template, request, jsonify

from app.contester.contester import Contester

api = Blueprint('api', __name__)
contester = Contester()


# API
@api.route('/send_code', methods=['POST'])
def send_code():
    data = request.json

    tests = contester.get_tests({})
    response = contester.run_tests(code=data['code'], language=data['lang'], tests=tests)

    return jsonify('', render_template('code_response_model.html', response=response))

@api.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    print(data)

    return jsonify('', 'OK')

@api.route('/get_task_input_block', methods=['POST'])
def get_task_input_block():
    data = request.json
    return jsonify('', render_template('admin/test_block_model.html', test_number=data['test_number']))