import subprocess
import sys

from flask import render_template, request, flash, redirect, url_for, session, jsonify

from web import app
from app.contester import contester

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/all-tasks')
def lessons_page():
    return render_template('lessons.html')


@app.route('/<int:grade>')
def grade_page(grade):
    return render_template('grade.html', grade=grade)


@app.route('/<int:grade>/<string:topic>')
def topic_page(grade, topic):
    return render_template('topic.html', grade=grade, topic=topic)


@app.route('/<int:grade>/<string:topic>/<int:task_number>')
def task_page(grade, topic, task_number):
    return render_template('task.html', grade=grade, topic=topic, task_number=task_number)


# API
@app.route('/api/send_code', methods=['POST'])
def send_code():
    data = request.json
    print(data['lang'])
    print(data['code'])

    tests = {
        '1\n2': '3',
        '1\n5': '6',
        '2\n5': '7',
        '5\n6': '11',
    }
    response = {'tests': {}}

    for index, (input_value, output_value) in enumerate(tests.items()):
        try:
            result = subprocess.run([sys.executable, "-c", data['code']], input=input_value, capture_output=True, text=True)
            answer = result.stdout.strip()
            error = result.stderr

            print(answer, output_value, error)

            assert answer == output_value

            print(f'Passed test number {index}')
            response['tests'][index + 1] = True

        except AssertionError:
            print(f'Failed test number {index}, incorrect answer')
            response['tests'][index + 1] = False

    passed_tests = len([result for result in response['tests'].values() if result])
    response['passed_tests'] = passed_tests

    return jsonify('', render_template('code_response_model.html', response=response))
