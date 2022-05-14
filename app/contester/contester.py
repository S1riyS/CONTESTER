import time
import pprint
from typing import Optional, List

import asyncio
import aiohttp
from flask_login import current_user

from app import app, db
from app.models import Submission, TestResult, Task, Test
from app.utils.fix_asyncio import silence_event_loop_closed
from app.utils.singleton import SingletonBaseClass

from .languages import languages
from .errors import ServerResponseError, ExecutionError, WrongAnswerError, TimeLimitError


class Contester(metaclass=SingletonBaseClass):
    def __init__(self, TESTING_MODE=False):
        self.API = 'https://wandbox.org/api/compile.json'  # API URL
        self.HEADERS = {'Content-Type': "application/json;charset=UTF-8"}  # Request headers
        self.TESTING_MODE = TESTING_MODE

    @staticmethod
    def _compare_answers(program_output: str, expected_output: str) -> Optional[WrongAnswerError]:
        if not program_output.strip() == expected_output.strip():
            raise WrongAnswerError

    @staticmethod
    def _get_number_of_passed_tests(tests: List[dict]) -> int:
        return len([result for result in tests if result['success']])

    @staticmethod
    def _save_to_database(task: Task, code: str, response: dict, language: str) -> None:
        """
        Method that saves all information about user's submission in database
        :param task: Task object
        :param code: User's code
        :param response: Dictionary with final response
        :param language: Programming language
        :return: None
        """
        passed_tests = response['passed_tests']

        submission = Submission(
            user_id=current_user.id,
            task_id=task.id,
            language=language,
            passed_tests=passed_tests,
            source_code=code
        )
        db.session.add(submission)
        db.session.commit()

        results = response['tests']

        for result in results:
            test_result = TestResult(
                test_id=result['test'].id,
                submission_id=submission.id,
                success=result['success'],
                message=result['message'],
                user_output=result['user_output']
            )
            db.session.add(test_result)

        db.session.commit()

    def load_from_db(self, submission: Submission) -> dict:
        results_array = []
        for result in submission.test_results:
            results_array.append({
                'message': result.message,
                'success': result.success,
                'user_output': result.user_output,
                'test': result.test
            })

        return {
            'language': languages.get_language(submission.language, object_only=True),
            'tests': results_array,
            'passed_tests': self._get_number_of_passed_tests(results_array)
        }

    async def _run_single_test(self, session: aiohttp.ClientSession, data: dict, current_test: Test) -> dict:
        """
        :param session: aiohttp.ClientSession() object
        :param data: params which will be passed in the request
        :param current_test: dictionary with test's data
        :return: Dictionary with result of test
        """
        response = {
            'success': None,
            'message': None,
            'user_output': None,
            'test': current_test
        }

        try:
            try:
                async with session.post(url=self.API, headers=self.HEADERS, json=data, timeout=10) as wandbox_response:
                    # Checking status code
                    if wandbox_response.status == 200:
                        result_json = await wandbox_response.json()  # Getting JSON

                        # Checking status
                        if result_json['status'] == '0':
                            response['user_output'] = result_json['program_output'].strip()

                            self._compare_answers(program_output=result_json['program_output'],
                                                  expected_output=current_test.test_output)
                        else:
                            raise ExecutionError  # Raising 'ExecutionError'
                    else:
                        raise ServerResponseError  # Raising 'ServerResponseError'

            except asyncio.TimeoutError:
                raise TimeLimitError  # Raising 'TimeLimitError'

        # Handling errors
        except (ServerResponseError, ExecutionError, WrongAnswerError, TimeLimitError) as error:
            response['success'] = False
            response['message'] = error.message

        # If everything OK
        else:
            response['success'] = True
            response['message'] = 'Success'

        return response

    async def _get_testing_results(self, code: str, language: str, task: Task) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param task: Task object
        :return: Dictionary with results of testing
        """
        response = {}  # Base of response
        current_language_dict = languages.get_language(language)

        if current_language_dict['success']:
            current_language = current_language_dict['language']
            compiler = current_language.compiler  # Getting compiler
            start_time = time.time()  # Getting time when tests were started

            async with aiohttp.ClientSession() as session:
                tasks = []

                for current_test in task.tests:
                    # Forming content of request
                    data = {
                        'code': code,
                        'compiler': compiler,
                        'stdin': current_test.test_input
                    }

                    # Creating asyncio task
                    asyncio_task = asyncio.ensure_future(self._run_single_test(session, data, current_test))
                    tasks.append(asyncio_task)

                test_results = await asyncio.gather(*tasks)  # Running tasks

                end_time = time.time()  # Getting time when tests were finished

                # Results of test
                response['tests'] = sorted(test_results, key=lambda item: item['success'])
                # Language
                response['language'] = current_language
                # Total time of testing
                response['time'] = "{0:.3f} sec".format(end_time - start_time)
                # Number of passed tests
                response['passed_tests'] = self._get_number_of_passed_tests(response['tests'])

                # Saving results to DB
                if not self.TESTING_MODE:
                    self._save_to_database(task=task, code=code, response=response, language=language)

                return response

        return None

    @silence_event_loop_closed
    def run_tests(self, code: str, language: str, task: Task) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param task: Task object
        :return: Dictionary with the results of testing the program
        """

        loop = asyncio.new_event_loop()  # Creating async loop
        response = loop.run_until_complete(self._get_testing_results(code, language, task))

        if app.config.get('TESTING'):
            pprint.pprint(response, indent=4)

        return response

contester = Contester()