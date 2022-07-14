"""
This is file with tests for Contester class (core of testing system)
"""
import unittest

from app.contester import Contester
from app.contester.utils import get_number_of_passed_tests
from app.contester.types import ContesterResponse, SingleTestResult

TESTING_CODE = {
    'python': {
        'success': """a, b = list(map(int, input().split()))\nprint(a + b)"""
    },
    'pascal': {
        'success': """var\n\ta, b:integer;\nbegin\n\treadln(a, b);\n\twriteln(a - b)\nend.""",
    },
    'cpp': {
        'success': """#include <iostream>\n\nusing namespace std;\n\nint main() {\n\tint a, b;\n\tcin >> a >> b;\n\tcout << a * b;\n}"""
    },
    'csharp': {
        'success': """using System;\n\nnamespace HelloWorld\n{\n\tclass Program\n\t{\n\t\tstatic void Main(string[] args)
        \n\t\t{\n\t\t\tstring[] num = Console.ReadLine().Split(' ');\n\t\t\tint a = int.Parse(num[0]);\n\t\t\tint b = int.Parse(num[1]);
        \n\t\t\tConsole.WriteLine(a + b);\n\t\t}\n\t}\n}"""
    }
}

TESTS = [

]


class ContesterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contester = Contester(TESTING_MODE=True)

    def test_get_number_of_passed_tests(self):
        test_results = (
            SingleTestResult(
                success=True,
                message='Success',
                test=None,
                user_output=None
            ),
            SingleTestResult(
                success=False,
                message='Wrong Answer',
                test=None,
                user_output=None
            ),
            SingleTestResult(
                success=True,
                message='Success',
                test=None,
                user_output=None
            ),
            SingleTestResult(
                success=False,
                message='Time Limit Error',
                test=None,
                user_output=None
            )
        )

        result = get_number_of_passed_tests(test_results)
        self.assertEqual(result, 2)

    def test_python_success(self):
        # Problem: sum two numbers (a + b)
        code = TESTING_CODE['python']['success']
        language = 'python'
        tests = [
            {
                'stdin': '1 2',
                'output': '3',
                'hidden': False
            }
        ]

        result = self.contester.run_tests(code, language, tests)
        self.assertIsNotNone(result)
        status = result['tests'][1]['status']
        self.assertEqual(status, Status.OK)

    def test_pypy_success(self):
        # Problem: sum two numbers (a + b)
        code = TESTING_CODE['python']['success']
        language = 'pypy'
        tests = [
            {
                'stdin': '1 2',
                'output': '3',
                'hidden': False
            }
        ]

        result = self.contester.run_tests(code, language, tests)
        self.assertIsNotNone(result)
        status = result['tests'][1]['status']
        self.assertEqual(status, Status.OK)

    def test_pascal_success(self):
        # Problem: subtract b from a (a - b)
        code = TESTING_CODE['pascal']['success']
        language = 'pascal'
        tests = [
            {
                'stdin': '21 5',
                'output': '16',
                'hidden': False
            }
        ]

        result = self.contester.run_tests(code, language, tests)
        self.assertIsNotNone(result)
        status = result['tests'][1]['status']
        self.assertEqual(status, Status.OK)

    def test_cpp_success(self):
        # Problem: multiply two numbers (a * b)
        code = TESTING_CODE['cpp']['success']
        language = 'cpp'
        tests = [
            {
                'stdin': '24 3',
                'output': '72',
                'hidden': True
            }
        ]

        result = self.contester.run_tests(code, language, tests)
        self.assertIsNotNone(result)
        status = result['tests'][1]['status']
        self.assertEqual(status, Status.OK)

    def test_csharp_success(self):
        # Problem: sum two numbers (a + b)
        code = TESTING_CODE['csharp']['success']
        language = 'csharp'
        tests = [
            {
                'stdin': '55 31',
                'output': '86',
                'hidden': True
            }
        ]

        result = self.contester.run_tests(code, language, tests)
        self.assertIsNotNone(result)
        status = result['tests'][1]['status']
        self.assertEqual(status, Status.OK)


if __name__ == "__main__":
    unittest.main()
