import subprocess
import sys

from flask import render_template, request, flash, redirect, url_for, session, jsonify

from . import app
from app.contester.contester import Contester, languages

contester = Contester()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/all-tasks', methods=['GET'])
def lessons_page():
    return render_template('lessons.html')


@app.route('/<int:grade>', methods=['GET'])
def grade_page(grade):
    return render_template('grade.html', grade=grade)


@app.route('/<int:grade>/<string:topic>', methods=['GET'])
def topic_page(grade, topic):
    return render_template('topic.html', grade=grade, topic=topic)


@app.route('/<int:grade>/<string:topic>/<int:task_number>', methods=['GET'])
def task_page(grade, topic, task_number):
    return render_template('task.html', grade=grade, topic=topic, task_number=task_number, languages=languages)


# API
@app.route('/api/send_code', methods=['POST'])
def send_code():
    data = request.json

    tests = contester.get_tests({})
    response = contester.run_tests(code_value=data['code'], language=data['lang'], tests=tests)

    return jsonify('', render_template('code_response_model.html', response=response))
