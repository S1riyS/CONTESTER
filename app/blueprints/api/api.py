from flask import Blueprint, render_template, request, jsonify, make_response
from sqlalchemy import and_

from app import db
from app.contester.contester import Contester

from app.models import Grade, Topic, Task, Example, Test

api = Blueprint('api', __name__)
contester = Contester()


# TODO: Переименоаить API (api/create/task и т.д.)

# API
@api.route('/send_code', methods=['POST'])
def send_code():
    data = request.json
    print(data)

    task = db.session.query(Task).filter(
        and_(
            Grade.number == data['path']['grade'],
            Topic.translit_name == data['path']['topic'],
            Task.translit_name == data['path']['task']
        )
    ).first()

    tests = task.get_tests()
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
    print(data)

    topic = Topic(
        grade_id=data['grade_id'],
        name=data['name']
    )
    topic.set_translit_name()

    if not db.session.query(Topic).filter(Topic.translit_name == topic.translit_name).first():
        db.session.add(topic)
        db.session.commit()

        return make_response(jsonify(
            {
                'success': True,
                'message': 'Тема успешно создана!'
            }
        ), 200)

    else:
        return make_response(jsonify(
            {
                'success': False,
                'message': 'Тема с таким именем уже существует'
            }
        ), 200)


@api.route('/create_task', methods=['POST'])
def create_task():
    data = request.json

    # Task
    task = Task(
        topic_id=data['path']['topic_id'],
        name=data['information']['name'],
        text=data['information']['condition']
    )
    task.set_translit_name()

    topic = db.session.query(Topic).filter(Topic.id == data['path']['topic_id']).first()
    translit_names = [task_.translit_name for task_ in topic.get_tasks()]

    if task.translit_name in translit_names:
        return make_response(jsonify(
            {
                'success': False,
                'message': 'Задача с таким именем уже существует'
            }
        ), 200)

    else:
        db.session.add(task)
        db.session.commit()

        # Example
        example = Example(
            task_id=task.id,
            example_input=data['example']['input'],
            example_output=data['example']['output']
        )
        db.session.add(example)

        # Tests
        tests = zip(data['tests']['inputs'], data['tests']['outputs'], data['tests']['is_hidden'])
        for test_input, test_output, is_hidden in tests:
            test = Test(
                task_id=task.id,
                test_input=test_input,
                test_output=test_output,
                is_hidden=is_hidden
            )
            db.session.add(test)

        db.session.commit()

    return make_response(jsonify(
        {
            'success': True,
            'message': 'Задача успешно создана'
        }
    ), 200)


@api.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json
    return jsonify({'status': 'OK'})


@api.route('/get_task_input_block', methods=['POST'])
def get_task_input_block():
    data = request.json
    return jsonify(render_template('responses/single_test_block.html', test_number=data['test_number']))
