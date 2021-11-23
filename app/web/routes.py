from flask import render_template, request, flash, redirect, url_for, session

from . import app


@app.route('/')
def hello_world():
    return render_template('base.html')
