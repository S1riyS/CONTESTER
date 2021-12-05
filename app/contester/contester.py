import requests
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

    def run_tests(self, code_value: str, language: str, tests: dict) -> dict:
        response = {'tests': {}}  # Base of response
        compiler = languages[language]['compiler']  # Getting compiler

        for index, (input_value, output_value) in enumerate(tests.items()):
            try:
                # Forming content of request
                data = {
                    'code': code_value,
                    'compiler': compiler,
                    'stdin': input_value
                }

                # Sending request to WandBox
                wandbox_response = requests.post(url=self.WANDBOX_COMPILE_URL,
                                                 json=data,
                                                 headers=self.HEADERS,
                                                 timeout=self.DEFAULT_TIMEOUT)

                # Checking status code
                if wandbox_response.status_code != 200:
                    raise ServerResponseException  # Raising 'ServerResponseException'

                else:
                    # Getting JSON
                    result_json = wandbox_response.json()  # JSON

                    # Checking status
                    if result_json['status'] == '0':
                        answer = result_json['program_output'].strip()  # Getting Answer
                        assert answer == output_value  # Checking answer

                        # If everything OK
                        response['tests'][index + 1] = {'status': 'OK', 'error': None}
                        print(f'Passed test number {index + 1}')
                    else:
                        raise ExecutionException  # Raising 'ExecutionException'


            except ServerResponseException:
                response['tests'][index + 1] = {'status': 'ERROR', 'error': 'Server Response Error'}
                print(f'Failed test number {index + 1}, Server Response Error')

            except ExecutionException:
                response['tests'][index + 1] = {'status': 'ERROR', 'error': 'Execution Error'}
                print(f'Failed test number {index + 1}, Execution Error')

            except requests.Timeout:
                response['tests'][index + 1] = {'status': 'ERROR', 'error': 'Timeout Error'}
                print(f'Failed test number {index + 1}, Timeout Error')

            except AssertionError:
                response['tests'][index + 1] = {'status': 'ERROR', 'error': 'Wrong Answer'}
                print(f'Failed test number {index + 1}, Wrong Answer')

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
