import unittest
from flask import session
from flask_login import login_user, current_user

from app import create_app, db
from app.models import User, Role, Grade, Topic, Task, init_db_data
from app.blueprints.api import utils
from app.blueprints.api.task import render_solution_failure, render_solution_success
from app.contester import ContesterResponse
from tests import TestConfig


def set_session_cookie(app, client):
    val = app.session_interface.get_signing_serializer(app).dumps(dict(session))
    client.set_cookie('localhost', app.session_cookie_name, val)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_send_alert(self):
        response = utils.send_alert(True, 'test_success')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'test_success')
        self.assertTrue(response.json['success'])

    def test_tests_to_orm_objects(self):
        # Dict with tests data
        tests = {
            'stdin_list': ['2 3'],
            'stdout_list': ['5'],
            'is_hidden_list': [False]
        }
        # Task object
        task = Task(
            topic_id=None,
            name='Test',
            text='test'
        )
        db.session.add(task)
        db.session.commit()
        # Executing tests_to_orm_objects function
        orm_objects = utils.tests_to_orm_objects(tests, task)
        test = orm_objects[0]

        self.assertEqual(test.stdin, '2 3')
        self.assertEqual(test.stdout, '5')
        self.assertEqual(test.is_hidden, False)


class TestAdminAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.global_grade = Grade(number=11)
        self.global_topic = Topic(name='Тема', grade_id=self.global_grade.id)
        self.global_topic.set_translit_name()
        db.session.add_all([self.global_grade, self.global_topic])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_topics(self):
        topic_1 = Topic(name='topic1', grade_id=self.global_grade.id)
        topic_2 = Topic(name='topic2', grade_id=self.global_grade.id)
        db.session.add_all([topic_1, topic_2])
        db.session.commit()

        response = self.client.post(
            '/api/topics',
            json={'grade_id': self.global_grade.id}
        )
        self.assertEqual(response.status_code, 200)

    def test_create_topic(self):
        response = self.client.post(
            '/api/admin/topic',
            json={'grade_id': self.global_grade.id, 'name': 'Имя темы'}
        )
        self.assertEqual(response.status_code, 200)

        # Editing topic

    def test_create_task(self):
        data = {
            'path': {
                'grade_id': self.global_grade.id,
                'topic_id': self.global_topic.id
            },
            'info': {
                'name': 'Имя',
                'condition': 'Условие'
            },
            'example': {
                'stdin': 'Пример ввода',
                'stdout': 'Пример вывода'
            },
            'tests': {
                'stdin_list': ['TEST1', 'TEST2'],
                'stdout_list': ['TEST1', 'TEST2'],
                'is_hidden_list': [True, False]}
        }

        # Creating topic
        response = self.client.post(
            '/api/admin/task',
            json=data
        )
        self.assertEqual(response.status_code, 200)


class TestTaskAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        init_db_data()
        self.client = self.app.test_client()

        self.global_grade = Grade(number=11)
        self.global_topic = Topic(name='Тема', grade=self.global_grade.id)
        self.global_topic.set_translit_name()
        self.global_task = Task(
            name='Задача',
            text='Условие',
            topic_id=self.global_topic.id
        )
        self.global_task.set_translit_name()
        db.session.add_all([self.global_grade, self.global_topic, self.global_task])
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_render_solution_failure(self):
        response = render_solution_failure(message='failure message example')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['result'])

    def test_render_solution_success(self):
        response = render_solution_success(response=ContesterResponse(
            language=None,
            tests=[],
            passed_tests=0,
            time=None
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['result'])

    def test_send_solution(self):
        with self.app.test_request_context():
            # Add user
            r = Role.query.filter_by(name='user').first()
            self.assertIsNotNone(r)
            user = User(name='имя', surname='фамилия', email='email@example.com', verified=True, role=r)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            # Sending solution
            data = {
                'path': {
                    'grade': self.global_grade.number,
                    'topic': self.global_topic.translit_name,
                    'task': self.global_task.translit_name
                },
                'code': 'print(1)',
                'lang': 'python',
                'partner_id': None
            }
            set_session_cookie(self.app, self.client)
            response = self.client.post(
                '/api/task/solution',
                json=data
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'OK')

    def test_send_report(self):
        with self.app.test_request_context():
            # Add user
            r = Role.query.filter_by(name='user').first()
            self.assertIsNotNone(r)
            user = User(name='имя', surname='фамилия', email='email@example.com', verified=True, role=r)
            db.session.add(user)
            db.session.commit()
            login_user(user)

            # Sending solution
            data = {
                'path': {
                    'grade': self.global_grade.number,
                    'topic': self.global_topic.translit_name,
                    'task': self.global_task.translit_name
                },
                'text': 'Текст жалобы'
            }
            set_session_cookie(self.app, self.client)
            response = self.client.post(
                '/api/task/report',
                json=data
            )
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
