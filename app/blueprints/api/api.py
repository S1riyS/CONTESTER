from flask import Blueprint, render_template, request, jsonify

from app import db
from app.contester.contester import Contester

from app.data.models import Grade, Topic

api = Blueprint('api', __name__)
contester = Contester()


# API
@api.route('/send_code', methods=['POST'])
def send_code():
    data = request.json
    print(data)

    tests = contester.get_tests({})
    response = contester.run_tests(code=data['code'], language=data['lang'], tests=tests)

    if response is not None:
        return jsonify(render_template('responses/code_success.html', response=response))
    else:
        return jsonify(render_template('responses/code_error.html'), count=5)


@api.route('/get_submissions', methods=['POST'])
def get_submissions():
    return jsonify(render_template('responses/submissions.html'))


@api.route('/send_report', methods=['POST'])
def send_report():
    data = request.json
    print(data)
    return jsonify({'status': 'OK'})

@api.route('/get_topics', methods=['POST'])
def get_topics():
    data = request.json
    grade = db.session.query(Grade).filter(Grade.id == data['grade_id']).first()
    topics = grade.get_topics()

    return jsonify(render_template('admin/dropdown/topic_list.html', topics=topics))


# Admin API
@api.route('/create_topic', methods=['POST'])
def create_topic():
    data = request.json

    topic = Topic(
        grade_id=data['grade_id'],
        name=data['name']
    )
    db.session.add(topic)
    db.session.commit()

    return jsonify('OK')


@api.route('/create_task', methods=['POST'])
def create_task():
    data = request.json
    print(data)

    for program_input, program_output in zip(data['tests']['inputsArray'], data['tests']['outputsArray']):
        # Do something with input and output
        ...

    return jsonify('OK')


@api.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json
    return jsonify({'status': 'OK'})


@api.route('/get_task_input_block', methods=['POST'])
def get_task_input_block():
    data = request.json
    return jsonify(render_template('responses/single_test_block.html', test_number=data['test_number']))
