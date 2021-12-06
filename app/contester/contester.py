import requests
from typing import Optional
import pprint

from .errors import ServerResponseException, ExecutionException

languages = {
    'cpp': {
        'name': 'C++',
        'compiler': 'gcc-head',
        'mode': 'text/x-c++src'},
    'csharp': {
        'name': 'C#',
        'compiler': 'mono-head',
        'mode': 'text/x-csharp'},
    'java': {
        'name': 'Java',
        'compiler': 'openjdk-head',
        'mode': 'text/x-java'},
    'python': {
        'name': 'Python 3',
        'compiler': 'cpython-head',
        'mode': 'text/x-python',
        'is_default': True},
    'pascal': {
        'name': 'Pascal',
        'compiler': 'fpc-head',
        'mode': 'text/x-pascal'},
}


class Contester:
    def __init__(self):
        self.WANDBOX_COMPILE_URL = 'https://wandbox.org/api/compile.json'
        self.DEFAULT_TIMEOUT = 2.75
        self.HEADERS = {
            'Content-Type': "application/json;charset=UTF-8",
        }

    def _send_wandbox_request(self, content: dict) -> requests.models.Response:
        # Sending request to WandBox
        return requests.post(url=self.WANDBOX_COMPILE_URL,
                             json=content,
                             headers=self.HEADERS,
                             timeout=self.DEFAULT_TIMEOUT)

    @staticmethod
    def _compare_answers(program_output: str, expected_output: str) -> Optional[AssertionError]:
        assert program_output.strip() == expected_output.strip()  # Checking answer

    def run_tests(self, code_value: str, language: str, tests: dict) -> dict:
        response = {'tests': {}}  # Base of response
        compiler = languages[language]['compiler']  # Getting compiler

        for index, (input_value, output_value) in enumerate(tests.items()):
            try:
                test_number = index + 1  # Calculating current test number

                # Forming content of request
                data = {
                    'code': code_value,
                    'compiler': compiler,
                    'stdin': input_value
                }

                # Sending request to WandBox
                wandbox_response = self._send_wandbox_request(content=data)

                # Checking status code
                if wandbox_response.status_code != 200:
                    raise ServerResponseException  # Raising 'ServerResponseException'

                else:
                    # Getting JSON
                    result_json = wandbox_response.json()  # JSON

                    # Checking status
                    if result_json['status'] == '0':
                        self._compare_answers(program_output=result_json['program_output'],
                                              expected_output=output_value)

                        # If everything OK
                        test_result = {'status': 'OK', 'error': None}
                        print(f'Passed test number {test_number}')

                    else:
                        raise ExecutionException  # Raising 'ExecutionException'

            # Exceptions block
            except ServerResponseException:
                test_result = {'status': 'ERROR', 'error': 'Server Response Error'}
                print(f'Failed test number {test_number}, Server Response Error')

            except ExecutionException:
                test_result = {'status': 'ERROR', 'error': 'Execution Error'}
                print(f'Failed test number {test_number}, Execution Error')

            except requests.Timeout:
                test_result = {'status': 'ERROR', 'error': 'Timeout Error'}
                print(f'Failed test number {test_number}, Timeout Error')

            except AssertionError:
                test_result = {'status': 'ERROR', 'error': 'Wrong Answer'}
                print(f'Failed test number {test_number}, Wrong Answer')

            finally:
                # Checking structure of result
                if test_result['status'] and (test_result['error'] is None or test_result['error']):
                    pass
                else:
                    test_result = {'status': 'ERROR', 'error': 'Testing System Error'}

                response['tests'][test_number] = test_result  # Writing result to response dictionary

        # Calculating total number of passed tests
        passed_tests = len([result for result in response['tests'].values() if result['status'] == 'OK'])
        response['passed_tests'] = passed_tests

        pprint.pprint(response, width=1)
        return response

    @staticmethod
    def get_tests(task: dict) -> dict:
        return {
            '1 2': '3',
            '1 5': '6',
            '2 5': '7',
            '5 6': '11',
        }
