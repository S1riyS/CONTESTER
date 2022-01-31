"""
This is file with tests for Contester class (core of testing system)
"""
import unittest

from app.contester.contester import Contester


class ContesterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contester = Contester()

    def test_compare_answers(self):
        result = self.contester._compare_answers(program_output=' 1 2 3', expected_output=' 1 2 3 ')
        self.assertIsNone(result)

    def test_get_number_of_passed_tests(self):
        tests = {1: {'status': 'OK', 'message': 'Success', 'info': {'stdin': '1 2', 'expected-output': '3'}},
                 2: {'status': 'ERROR', 'message': 'Wrong Answer', 'info': {'stdin': '1 5', 'expected-output': '6'}},
                 3: {'status': 'OK', 'message': 'Success', 'info': None},
                 4: {'status': 'ERROR', 'message': 'Time Limit Error', 'info': None}}
        result = self.contester._get_number_of_passed_tests(tests)
        self.assertEqual(result, 2)

    def test_python_success(self):
        # Problem: sum two numbers (a + b)
        code = """a, b = list(map(int, input().split()))\nprint(a + b)"""
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
        message = result['tests'][1]['message']
        self.assertEqual(message, 'Success')

    def test_pypy_success(self):
        # Problem: sum two numbers (a + b)
        code = """a, b = list(map(int, input().split()))\nprint(a + b)"""
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
        message = result['tests'][1]['message']
        self.assertEqual(message, 'Success')

    def test_pascal_success(self):
        # Problem: subtract b from a (a - b)
        code = """var\n\ta, b:integer;\nbegin\n\treadln(a, b);\n\twriteln(a - b)\nend."""
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
        message = result['tests'][1]['message']
        self.assertEqual(message, 'Success')

    def test_cpp_success(self):
        # Problem: multiply two numbers (a * b)
        code = """#include <iostream>\n\nusing namespace std;\n\nint main() {\n\tint a, b;\n\tcin >> a >> b;\n\tcout << a * b;\n}"""
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
        message = result['tests'][1]['message']
        self.assertEqual(message, 'Success')

    def test_csharp_success(self):
        # Problem: sum two numbers (a + b)
        code = """using System;

        namespace HelloWorld
        {
            class Program
            {
                static void Main(string[] args)
                {
                    string[] num = Console.ReadLine().Split(' ');
                    int a = int.Parse(num[0]);
                    int b = int.Parse(num[1]);
                    Console.WriteLine(a + b);
                }
            }
        }"""

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
        message = result['tests'][1]['message']
        self.assertEqual(message, 'Success')


if __name__ == "__main__":
    unittest.main()
