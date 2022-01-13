import time
import pprint
from typing import Optional

import asyncio
import aiohttp

from .errors import TestingSystemError, ServerResponseError, ExecutionError, WrongAnswerError, ExecutionTimeoutError

# Dictionary with programming languages (name, compiler, CodeMirror mode)
languages = {
    'cpp': {
        'name': 'C++',
        'compiler': 'gcc-head',
        'mode': 'text/x-c++src'},
    'csharp': {
        'name': 'C#',
        'compiler': 'mono-6.12.0.122',
        'mode': 'text/x-csharp'},
    'python': {
        'name': 'Python 3.8.9',
        'compiler': 'cpython-3.8.9',
        'mode': 'text/x-python',
        'is_default': True},
    'pascal': {
        'name': 'Pascal',
        'compiler': 'fpc-3.2.0',
        'mode': 'text/x-pascal'},
}


class Contester:
    def __init__(self):
        self.API_URL = 'https://wandbox.org/api/compile.json'  # API URL
        self.HEADERS = {'Content-Type': "application/json;charset=UTF-8"}  # Request headers

    @staticmethod
    def _get_compiler(language) -> str:
        if language in languages:
            return languages[language]['compiler']
        else:
            return None

    @staticmethod
    def _compare_answers(program_output, expected_output) -> Optional[WrongAnswerError]:
        if not program_output.strip() == expected_output.strip():
            raise WrongAnswerError

    @staticmethod
    def _get_number_of_passed_tests(tests) -> int:
        return len([result for result in tests.values() if result['status'] == 'OK'])

    async def _run_single_test(self, session, data, current_test, test_number) -> dict:
        """
        :param session: aiohttp.ClientSession() object
        :param data: params which will be passed in the request
        :param test_number: Number of test
        :return: Dictionary with result of test
        """
        response = {}
        result = {'status': None, 'message': None}

        try:
            try:
                async with session.post(url=self.API_URL, headers=self.HEADERS, json=data, timeout=10) as wandbox_response:
                    # Checking status code
                    if wandbox_response.status == 200:
                        result_json = await wandbox_response.json()  # Getting JSON

                        # Checking status
                        if result_json['status'] == '0':
                            self._compare_answers(program_output=result_json['program_output'],
                                                  expected_output=current_test['output'])
                        else:
                            raise ExecutionError  # Raising 'ExecutionError'
                    else:
                        raise ServerResponseError  # Raising 'ServerResponseError'

            except asyncio.TimeoutError:
                raise ExecutionTimeoutError

        # Handling errors
        except (ServerResponseError, ExecutionError, WrongAnswerError, ExecutionTimeoutError) as error:
            result = {'status': 'ERROR', 'message': error.message}
            print(f'Failed test number {test_number}, {error.message}')

        # If everything OK
        else:
            result = {'status': 'OK', 'message': 'Success'}
            print(f'Passed test number {test_number}')

        finally:
            # Checking if test can be shown
            if not current_test['hidden']:
                result['info'] = {'stdin': current_test['stdin'], 'expected-output': current_test['output']}
            else:
                result['info'] = None

            response['test_number'] = test_number  # Writing test number to response
            response['result'] = result  # Writing result to response

        return response

    async def _get_testing_results(self, code, language, tests) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param tests: Dictionary with tests
        :return: None
        """
        compiler = self._get_compiler(language)  # Getting compiler

        if compiler is not None:
            response = {'tests': {}}  # Base of response

            start_time = time.time() # Getting time when tests were started

            async with aiohttp.ClientSession() as session:
                tasks = []

                for index, current_test in enumerate(tests):
                    # Forming content of request
                    data = {
                        'code': code,
                        'compiler': compiler,
                        'stdin': current_test['stdin']
                    }

                    # Creating asyncio task
                    task = asyncio.ensure_future(self._run_single_test(session, data, current_test, index))
                    tasks.append(task)

                test_results = await asyncio.gather(*tasks)  # Running tasks

                # Writing sub-dictionary with results of testing to response
                for test_result in test_results:
                    test_number = test_result['test_number'] + 1
                    response['tests'][test_number] = test_result['result']

                end_time = time.time() # Getting time when tests were finished

                # Total time of testing
                response['time'] = end_time - start_time
                # Compiler
                response['compiler'] = compiler
                # Total number of passed tests
                response['passed_tests'] = self._get_number_of_passed_tests(response['tests'])
                return response

        return None

    def run_tests(self, code, language, tests) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param tests: Dictionary with tests
        :return: Dictionary with the results of testing the program
        """

        loop = asyncio.new_event_loop()  # Creating async loop
        response = loop.run_until_complete(self._get_testing_results(code, language, tests))

        pprint.pprint(response, width=1)
        return response

    @staticmethod
    def get_tests(task=None) -> dict:
        return [
            {
                'stdin': '1 2',
                'output': '3',
                'hidden': False
            },
            {
                'stdin': '1 5',
                'output': '6',
                'hidden': False
            },
            {
                'stdin': '2 5',
                'output': '7',
                'hidden': True
            },
            {
                'stdin': '5 6',
                'output': '11',
                'hidden': True
            },
            {
                'stdin': '5 6',
                'output': '11',
                'hidden': True
            },
            {
                'stdin': '7 8',
                'output': '15',
                'hidden': True
            },
            {
                'stdin': '50 6',
                'output': '56',
                'hidden': True
            },
            {
                'stdin': '51 61',
                'output': '112',
                'hidden': True
            },
            {
                'stdin': '10 5',
                'output': '15',
                'hidden': True
            },
            {
                'stdin': '11 11',
                'output': '22',
                'hidden': True
            },
            {
                'stdin': '34 34',
                'output': '68',
                'hidden': True
            }
        ]
