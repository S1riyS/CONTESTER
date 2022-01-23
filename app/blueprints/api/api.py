from flask import Blueprint, render_template, request, jsonify
import time
from app.contester.contester import Contester

api = Blueprint('api', __name__)
contester = Contester()


# API
@api.route('/send_code', methods=['POST'])
def send_code():
    data = request.json

    tests = contester.get_tests({})
    response = contester.run_tests(code=data['code'], language=data['lang'], tests=tests)

    if response is not None:
        return jsonify(render_template('response_models/code_success.html', response=response))
    else:
        return jsonify(render_template('response_models/code_error.html'), count=5)


@api.route('/get_submissions', methods=['POST'])
def get_submissions():
    time.sleep(1)
    return jsonify(render_template('response_models/submissions.html'))


@api.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    print(data)

    for program_input, program_output in zip(data['tests']['inputsArray'], data['tests']['outputsArray']):
        # Do something with input and output
        ...

    return jsonify('OK')


@api.route('/get_task_input_block', methods=['POST'])
def get_task_input_block():
    data = request.json
    return jsonify(render_template('admin/test_block_model.html', test_number=data['test_number']))
