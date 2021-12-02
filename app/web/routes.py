from flask import render_template, request, flash, redirect, url_for, session

from . import app


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/all-tasks')
def lessons_page():
    return render_template('lessons.html')

@app.route('/<int:grade>-grade')
def grade_page(grade):
    return render_template('grade.html', grade=grade)

@app.route('/<int:grade>-grade/<string:topic>')
def topic_page(grade, topic):
    return render_template('topic.html', grade=grade, topic=topic)

@app.route('/<int:grade>-grade/<string:topic>/<int:task_number>')
def task_page(grade, topic, task_number):
    return render_template('task.html', grade=grade, topic=topic, task_number=task_number)
