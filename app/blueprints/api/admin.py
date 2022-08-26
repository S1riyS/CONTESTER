"""
Module with Admin APIs
"""

from flask import request, make_response, jsonify, url_for

from app import db
from app.models import Grade, Topic, Task, Example, load_user
from app.blueprints.api import api
from .utils import send_alert, tests_to_orm_objects


@api.route('/topics', methods=['POST'])
def get_topics():
    data = request.json
    grade = db.session.query(Grade).filter(Grade.id == data['grade_id']).first()

    topics_array = []
    for topic in grade.topics:
        topics_array.append({
            'id': topic.id,
            'name': topic.name
        })

    return jsonify({'topics': topics_array})


@api.route('/admin/topic', methods=['POST'])
def create_topic():
    data = request.json

    topic = Topic(
        grade_id=data['grade_id'],
        name=data['name'].strip()
    )
    topic.set_translit_name()

    if not db.session.query(Topic).filter(Topic.translit_name == topic.translit_name).first():
        db.session.add(topic)
        db.session.commit()

        return send_alert(True, 'Тема успешно создана!')
    else:
        return send_alert(False, 'Тема с таким именем уже существует')


@api.route('/admin/topic/<topic_id>', methods=['PUT'])
def update_topic(topic_id):
    data = request.json

    try:
        topic = db.session.query(Topic).get(topic_id)

        # Updating general info
        topic.grade_id = data['grade_id']
        topic.name = data['name']
        db.session.commit()

        return send_alert(True, 'Тема успешно обновлена!')

    except Exception:
        return send_alert(False, 'Не удалось обновить тему')


@api.route('/admin/task', methods=['POST'])
def create_task():
    data = request.json

    # Task
    task = Task(
        topic_id=data['path']['topic_id'],
        name=data['info']['name'].strip(),
        text=data['info']['condition'].strip()
    )
    task.set_translit_name()

    # Checking whether a task with this name already exists
    topic = db.session.query(Topic).get(data['path']['topic_id'])
    translit_names = [task_.translit_name for task_ in topic.tasks]
    if task.translit_name in translit_names:
        return send_alert(False, 'Задача с таким именем уже существует')

    else:
        db.session.add(task)
        db.session.commit()

        # Example
        example = Example(
            task_id=task.id,
            example_input=data['example']['stdin'],
            example_output=data['example']['stdout']
        )
        db.session.add(example)

        # Tests
        tests_to_orm_objects(data['tests'], task)

    return send_alert(True, 'Задача успешно создана')


@api.route('/admin/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    try:
        task = db.session.query(Task).get(task_id)

        # Updating general info
        task.topic_id = data['path']['topic_id']
        task.name = data['info']['name'].strip()
        task.text = data['info']['condition'].strip()
        task.set_translit_name()

        # Updating example
        task.example.example_input = data['example']['stdin']
        task.example.example_output = data['example']['stdout']

        # Deleting old tests
        for test in task.tests:
            db.session.delete(test)
        db.session.commit()

        # Adding new tests
        tests_to_orm_objects(data['tests'], task)

        return send_alert(True, 'Задача успешно обновлена')

    except Exception:
        return send_alert(False, 'Не удалось обновить задачу')


@api.route('/admin/task', methods=['DELETE'])
def delete_task():
    data = request.json

    task = db.session.query(Task).get(data['task_id'])
    topic_url = url_for(
        'problems.topic_page',
        grade_number=task.topic.grade.number,
        topic_translit_name=task.topic.translit_name
    )

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({'success': True, 'redirect_url': topic_url}), 200)


@api.route('/admin/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = load_user(user_id)
    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({'success': True, 'redirect_url': url_for('home_page')}), 200)
