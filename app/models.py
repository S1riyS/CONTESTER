from os import environ
import datetime

import sqlalchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from transliterate import slugify

from app import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"))
    role = relationship('Role')

    grade_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("grades.id"))
    grade = relationship('Grade')
    grade_letter = sqlalchemy.Column(sqlalchemy.String)

    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    registration_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Grade(db.Model):
    __tablename__ = "grades"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def get_topics(self):
        return db.session.query(Topic).filter(Topic.grade_id == self.id).all()


class Role(db.Model):
    __tablename__ = "roles"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Topic(db.Model):
    __tablename__ = "topics"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    grade_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("grades.id"))
    grade = relationship('Grade')

    name = sqlalchemy.Column(sqlalchemy.String)
    translit_name = sqlalchemy.Column(sqlalchemy.String)

    def set_translit_name(self):
        self.translit_name = slugify(self.name)

    def get_tasks(self):
        return db.session.query(Task).filter(Task.topic_id == self.id).all()


class Task(db.Model):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))
    topic = relationship('Topic')

    name = sqlalchemy.Column(sqlalchemy.String)
    translit_name = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.Text)

    tests = relationship('Test', backref='tasks', lazy='subquery')

    def set_translit_name(self):
        self.translit_name = slugify(self.name)

    def get_example(self):
        return db.session.query(Example).filter(Example.task_id == self.id).first()

    def get_tests(self):
        return db.session.query(Test).filter(Test.task_id == self.id).all()


class Example(db.Model):
    __tablename__ = "examples"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = relationship('Task')

    example_input = sqlalchemy.Column(sqlalchemy.Text)
    example_output = sqlalchemy.Column(sqlalchemy.Text)


class Test(db.Model):
    __tablename__ = "tests"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = relationship('Task')

    test_input = sqlalchemy.Column(sqlalchemy.Text)
    test_output = sqlalchemy.Column(sqlalchemy.Text)
    is_hidden = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    def __repr__(self):
        return f'Test: Input: {self.test_input}, Output: {self.test_output}, Hidden: {self.is_hidden}'


class Submission(db.Model):
    __tablename__ = "submissions"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = relationship('User')

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = relationship('Task')

    language = sqlalchemy.Column(sqlalchemy.String)
    passed_tests = sqlalchemy.Column(sqlalchemy.Integer)
    source_code = sqlalchemy.Column(sqlalchemy.Text)
    submission_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)

    test_results = relationship('TestResult', backref="submission", lazy='subquery')

    def get_result(self) -> dict:
        failed_tests = [result for result in self.test_results if not result.success]
        if any(failed_tests):
            failed_test = failed_tests[0]
            return {'success': False, 'message': failed_test.message}

        return {'success': True, 'message': 'Success'}


class TestResult(db.Model):
    __tablename__ = "test_result"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    test = relationship('Test')

    submission_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("submissions.id"))


    success = sqlalchemy.Column(sqlalchemy.Boolean)
    message = sqlalchemy.Column(sqlalchemy.String)
    user_output = sqlalchemy.Column(sqlalchemy.String)


class Report(db.Model):
    __tablename__ = "reports"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = relationship('User')

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = relationship('Task')

    text = sqlalchemy.Column(sqlalchemy.Text)


def init_db_data():
    # Creating grades
    if db.session.query(User).count() == 0:
        for grade in range(5, 12):
            db.session.add(Grade(number=grade))

        # Creating roles
        user_role = Role(name='user')
        db.session.add(user_role)
        admin_role = Role(name='admin')
        db.session.add(admin_role)

        # Creating admin
        admin = User(
            name='Админ',
            surname='Админович',
            email='contester@mail.ru',
            verified=True,
            role_id=db.session.query(Role).filter(Role.name == 'admin').first().id,
            grade_id=None,
            grade_letter=None
        )
        admin.set_password(environ.get('ADMIN_PASSWORD'))
        db.session.add(admin)

        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
