from flask import render_template, request, flash, redirect, url_for, session

from . import app


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/lessons')
def lessons_page():
    return render_template('lessons.html')


@app.route('/lessons/<int:grade>-grade/<string:topic>/<int:task_number>')
def task_page(grade, topic, task_number):
    return render_template('task.html', grade=grade, topic=topic, task_number=task_number)
