"""
This is file with tests for Contester class (core of testing system)
"""
import unittest

from app.contester import Contester

test_code = {
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


class ContesterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contester = Contester()

    def test_compare_answers(self):
        result = self.contester._compare_answers(program_output=' 1 2 3', expected_output=' 1 2 3 ')
        self.assertIsNone(result)

    def test_get_number_of_passed_tests(self):
        tests = {1: {'success': True, 'message': 'Success', 'info': {'stdin': '1 2', 'expected-output': '3'}},
                 2: {'success': False, 'message': 'Wrong Answer', 'info': {'stdin': '1 5', 'expected-output': '6'}},
                 3: {'success': True, 'message': 'Success', 'info': None},
                 4: {'success': False, 'message': 'Time Limit Error', 'info': None}}

        result = self.contester._get_number_of_passed_tests(tests)
        self.assertEqual(result, 2)

    def test_python_success(self):
        # Problem: sum two numbers (a + b)
        code = test_code['python']['success']
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
        code = test_code['python']['success']
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
        code = test_code['pascal']['success']
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
        code = test_code['cpp']['success']
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
        code = test_code['csharp']['success']
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
