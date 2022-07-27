import typing as t

from flask_wtf import FlaskForm

from app import db
from app.models import Grade, Topic


def init_grades_select(form: FlaskForm) -> None:
    grades = db.session.query(Grade).all()
    grades_tuple = [(grade.id, grade.number) for grade in grades]
    form.grade_id.choices = grades_tuple


def init_topics_select(form: FlaskForm, grade_id: t.Optional[int] = None) -> None:
    if not grade_id:
        grade_id = form.grade_id.choices[0][0]  # [(grade.id <- this value, grade.number), ...]

    topics = db.session.query(Topic).filter_by(grade_id=grade_id).all()
    topics_tuple = [(topic.id, topic.name) for topic in topics]
    form.topic_id.choices = topics_tuple
