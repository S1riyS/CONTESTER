from flask import render_template, request, flash, redirect, url_for, session

from . import app


@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/lessons')
def lessons_page():
    return render_template('lessons.html')