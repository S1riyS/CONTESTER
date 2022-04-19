import time
import pprint
from typing import Optional, List

import asyncio
import aiohttp
from flask_login import current_user

from app import app, db
from app.models import Submission, TestResult
from .errors import TestingSystemError, ServerResponseError, ExecutionError, WrongAnswerError, TimeLimitError
from .fix_asyncio import silence_event_loop_closed

# Dictionary with programming languages (name, compiler, CodeMirror mode)
languages = {
    'cpp': {
        'name': 'C++',
        'fullname': 'GNU C++ 11.1',
        'compiler': 'gcc-11.1.0',
        'mode': 'text/x-c++src',
        'icon': 'cpp.svg'},
    'csharp': {
        'name': 'C#',
        'fullname': 'C# Mono 6.12',
        'compiler': 'mono-6.12.0.122',
        'mode': 'text/x-csharp',
        'icon': 'csharp.svg'},
    'python': {
        'name': 'Python 3',
        'fullname': 'Python 3.8.9',
        'compiler': 'cpython-3.8.9',
        'mode': 'text/x-python',
        'icon': 'python.svg',
        'is_default': True},
    'pypy': {
        'name': 'Pypy 3',
        'fullname': 'Pypy 3.7 (7.3.4)',
        'compiler': 'pypy-3.7-v7.3.4',
        'mode': 'text/x-python',
        'icon': 'python.svg'},
    'pascal': {
        'name': 'Pascal',
        'fullname': 'Free Pascal 3.2.0',
        'compiler': 'fpc-3.2.0',
        'mode': 'text/x-pascal',
        'icon': 'default.svg'},
}


class Contester:
    def __init__(self):
        self.API = 'https://wandbox.org/api/compile.json'  # API URL
        self.HEADERS = {'Content-Type': "application/json;charset=UTF-8"}  # Request headers

    @staticmethod
    def _compare_answers(program_output: str, expected_output: str) -> Optional[WrongAnswerError]:
        if not program_output.strip() == expected_output.strip():
            raise WrongAnswerError

    @staticmethod
    def _get_number_of_passed_tests(tests: List[dict]) -> int:
        return len([result for result in tests if result['success']])

    async def _run_single_test(self, session: aiohttp.ClientSession, data: dict, current_test: dict) -> dict:
        """
        :param session: aiohttp.ClientSession() object
        :param data: params which will be passed in the request
        :return: Dictionary with result of test
        """
        response = {'status': None, 'message': None}

        try:
            try:
                async with session.post(url=self.API, headers=self.HEADERS, json=data, timeout=10) as wandbox_response:
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
                raise TimeLimitError  # Raising 'TimeLimitError'

        # Handling errors
        except (ServerResponseError, ExecutionError, WrongAnswerError, TimeLimitError) as error:
            response = {'success': False, 'message': error.message}

        # If everything OK
        else:
            response = {'success': True, 'message': 'Success'}

        finally:
            # Checking if test can be shown
            if not current_test['hidden']:
                response['info'] = {'stdin': current_test['stdin'], 'expected-output': current_test['output']}

        return response

    async def _get_testing_results(self, code: str, language: str, tests: List[dict]) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param tests: Dictionary with tests
        :return: Dictionary with results of testing
        """
        response = {'tests': {}}  # Base of response
        current_language = languages.get(language, None)

        if current_language is not None:
            compiler = current_language['compiler']  # Getting compiler
            start_time = time.time()  # Getting time when tests were started

            async with aiohttp.ClientSession() as session:
                tasks = []

                for current_test in tests:
                    # Forming content of request
                    data = {
                        'code': code,
                        'compiler': compiler,
                        'stdin': current_test['stdin']
                    }

                    # Creating asyncio task
                    task = asyncio.ensure_future(self._run_single_test(session, data, current_test))
                    tasks.append(task)

                test_results = await asyncio.gather(*tasks)  # Running tasks

                end_time = time.time()  # Getting time when tests were finished

                # Results of test
                response['tests'] = sorted(test_results, key=lambda item: item['success'])
                # Language
                response['language'] = {'fullname': current_language['fullname'], 'icon': current_language['icon']}
                # Total time of testing
                response['time'] = "{0:.3f} sec".format(end_time - start_time)
                # Number of passed tests
                response['passed_tests'] = self._get_number_of_passed_tests(response['tests'])

                # submission = Submission(
                #     user_id=current_user.id,
                #
                # )

                return response

        return None

    @silence_event_loop_closed
    def run_tests(self, code: str, language: str, tests: List[dict]) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param tests: Dictionary with tests
        :return: Dictionary with the results of testing the program
        """

        loop = asyncio.new_event_loop()  # Creating async loop
        response = loop.run_until_complete(self._get_testing_results(code, language, tests))

        if app.config.get('TESTING'):
            pprint.pprint(response, indent=4)

        return response
