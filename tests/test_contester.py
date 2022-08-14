import unittest
import typing as t

from app import create_app, db
from app.contester import Contester
from app.contester.types import ContesterResponse
from app.models import Task, Test
from tests import TestConfig

TESTING_CODE = {
    'python': {
        'success': """a, b = list(map(int, input().split()))\nprint(a + b)"""
    },
    'pypy': {
        'success': """a, b = list(map(int, input().split()))\nprint(a + b)"""
    },
    'pascal': {
        'success': """var\n\ta, b:Longint;\nbegin\n\treadln(a, b);\n\twriteln(a + b)\nend.""",
    },
    'cpp': {
        'success': """#include <iostream>\n\nusing namespace std;\n\nint main() {
        \n\tint a, b;\n\tcin >> a >> b;\n\tcout << a + b;\n}"""
    },
    'csharp': {
        'success': """using System;\n\nnamespace HelloWorld\n{\n\tclass Program\n\t{\n\t\t
        static void Main(string[] args)
        \n\t\t{\n\t\t\tstring[] num = Console.ReadLine().Split(' ');\n\t\t\t
        int a = int.Parse(num[0]);\n\t\t\tint b = int.Parse(num[1]);
        \n\t\t\tConsole.WriteLine(a + b);\n\t\t}\n\t}\n}"""
    }
}


class ContesterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.contester = Contester(TESTING_MODE=True)

        self.task = Task(name='Сложение', text='Сложить два числа')
        self.task.set_translit_name()
        db.session.add(self.task)
        db.session.commit()

        self.tests = [
            Test(stdin='2 2', stdout='4', is_hidden=False, task_id=self.task.id),
            Test(stdin='4 5', stdout='9', is_hidden=False, task_id=self.task.id),
            Test(stdin='10 -10', stdout='0', is_hidden=True, task_id=self.task.id),
            Test(stdin='123192834 9829184', stdout='133022018', is_hidden=True, task_id=self.task.id)
        ]
        db.session.add_all(self.tests)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def __process_result(self, result: ContesterResponse):
        self.assertIsNotNone(result)  # Testing system has returned correct response
        self.assertEqual(len(result.tests), len(self.task.tests))  # Response contains results of all tests
        self.assertEqual(result.passed_tests, len(self.task.tests))  # All tests are passed
        self.assertIsNotNone(result.language)  # Language is defined

    def test_python_success(self):
        language = 'python'
        code = TESTING_CODE[language]['success']
        result = self.contester.run_tests(code, language, self.task)
        self.__process_result(result)

    def test_pypy_success(self):
        language = 'pypy'
        code = TESTING_CODE[language]['success']
        result = self.contester.run_tests(code, language, self.task)
        self.__process_result(result)

    def test_pascal_success(self):
        language = 'pascal'
        code = TESTING_CODE[language]['success']
        result = self.contester.run_tests(code, language, self.task)
        print(result)
        self.__process_result(result)

    def test_cpp_success(self):
        language = 'cpp'
        code = TESTING_CODE[language]['success']
        result = self.contester.run_tests(code, language, self.task)
        self.__process_result(result)

    def test_csharp_success(self):
        language = 'csharp'
        code = TESTING_CODE[language]['success']
        result = self.contester.run_tests(code, language, self.task)
        self.__process_result(result)


if __name__ == "__main__":
    unittest.main()
