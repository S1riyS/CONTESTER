import datetime

import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from utils import ru2en_transliteration


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"))
    role = orm.relation('Role')

    grade_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("grades.id"))
    grade = orm.relation('Grade')
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
    # TODO: Пофиксить __init__

    __tablename__ = "topics"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    grade_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("grades.id"))
    grade = orm.relation('Grade')

    name = sqlalchemy.Column(sqlalchemy.String)
    translit_name = sqlalchemy.Column(sqlalchemy.String)

    def set_translit_name(self):
        self.translit_name = ru2en_transliteration(self.name)


class Task(db.Model):
    # TODO: Пофиксить __init__

    __tablename__ = "tasks"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))
    topic = orm.relation('Topic')

    name = sqlalchemy.Column(sqlalchemy.String)
    translit_name = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.Text)

    def set_translit_name(self):
        self.translit_name = ru2en_transliteration(self.name)


class Example(db.Model):
    __tablename__ = "examples"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = orm.relation('Task')

    example_input = sqlalchemy.Column(sqlalchemy.Text)
    example_output = sqlalchemy.Column(sqlalchemy.Text)


class Test(db.Model):
    __tablename__ = "tests"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = orm.relation('Task')

    test_input = sqlalchemy.Column(sqlalchemy.Text)
    test_output = sqlalchemy.Column(sqlalchemy.Text)
    is_hidden = sqlalchemy.Column(sqlalchemy.Boolean, default=True)


class Report(db.Model):
    __tablename__ = "reports"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = orm.relation('Task')

    text = sqlalchemy.Column(sqlalchemy.Text)


class Submission(db.Model):
    __tablename__ = "submissions"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"))
    task = orm.relation('Task')

    language = sqlalchemy.Column(sqlalchemy.String)
    passed_tests = sqlalchemy.Column(sqlalchemy.Integer)
    source_code = sqlalchemy.Column(sqlalchemy.Text)
    submission_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)


def init_db_data():
    db_session = db.session  # DB session

    # Creating grades
    if db_session.query(User).count() == 0:
        for grade in range(5, 12):
            db_session.add(Grade(number=grade))

        print(db_session.query(Grade).filter(Grade.number == 10).first().id)

        # Creating roles
        user_role = Role(name='user')
        db_session.add(user_role)
        admin_role = Role(name='admin')
        db_session.add(admin_role)

        # Creating admin
        admin = User(
            name='Админ',
            surname='Админович',
            role_id=db_session.query(Role).filter(Role.name == 'admin').first().id,
            grade_id=None,
            grade_letter=None
        )
        admin.set_password('secret_admin_password')
        db_session.add(admin)

        # Creating user
        user = User(
            name='Обычный',
            surname='Пользователь',
            role_id=db_session.query(Role).filter(Role.name == 'user').first().id,
            grade_id=db_session.query(Grade).filter(Grade.number == 10).first().id,
            grade_letter='А'
        )
        user.set_password('secret_user_password')
        db_session.add(user)

        db_session.commit()
