import typing as t
import time
import pprint

import asyncio
import aiohttp
from flask_login import current_user

from app import app, db
from app.models import User, Submission, TestResult, Task, Test
from app.utils.fix_asyncio import silence_event_loop_closed
from app.utils.singleton import SingletonBaseClass

from .api_service import ApiCall, ApiCallData
from .languages import Language, languages
from .utils import get_number_of_passed_tests
from .types import SingleTestResult, ContesterResponse
from .exceptions import ContesterError, ApiServiceError, ExecutionError, WrongAnswerError, TimeOutError


class Contester(metaclass=SingletonBaseClass):
    def __init__(self, TESTING_MODE=False):
        self.TESTING_MODE = TESTING_MODE

    @staticmethod
    def __save_to_database(
            task: Task,
            code: str,
            response: ContesterResponse,
            language: str,
            partner: t.Optional[User] = None
    ) -> None:
        """Saves all information about user's submission in database"""
        submission = Submission(
            task_id=task.id,
            language=language,
            passed_tests=response.passed_tests,
            source_code=code
        )
        db.session.add(submission)
        db.session.commit()

        current_user.submissions.append(submission)
        if partner:
            partner.submissions.append(submission)
        db.session.commit()

        for result in response.tests:
            test_result = TestResult(
                test_id=result.test.id,
                submission_id=submission.id,
                success=result.success,
                message=result.message,
                user_output=result.user_output
            )
            db.session.add(test_result)
        db.session.commit()

    def load_from_db(self, submission: Submission) -> ContesterResponse:
        """ Returns `ContesterResponse` object with all data of submission"""
        results_array = []
        for result in submission.test_results:
            results_array.append(SingleTestResult(
                message=result.message,
                success=result.success,
                user_output=result.user_output,
                test=result.test
            ))

        return ContesterResponse(
            language=languages.get_language(submission.language, object_only=True),
            tests=results_array,
            passed_tests=get_number_of_passed_tests(results_array),
            time='None sec'
        )

    @staticmethod
    async def __run_single_test(
            session: aiohttp.ClientSession,
            data: ApiCallData,
            current_test: Test
    ) -> SingleTestResult:
        """Returns result of a single test"""
        try:
            api_call = ApiCall(session, data, current_test.test_output)
            await api_call.run()

        # Handling errors
        except ContesterError as error:
            success = False
            message = error.message

        # Everything OK
        else:
            success = True
            message = 'Success'

        user_output = api_call.user_output
        return SingleTestResult(
            message=message,
            success=success,
            test=current_test,
            user_output=user_output
        )

    async def __get_testing_results(self, code: str, language: str, task: Task) -> ContesterResponse:
        """Asynchronously runs all tests and returns `ContesterResponse` object"""
        current_language_dict = languages.get_language(language)

        if current_language_dict['success']:
            current_language = current_language_dict['language']
            compiler = current_language.compiler
            start_time = time.time()

            async with aiohttp.ClientSession() as session:
                tasks = []

                for current_test in task.tests:
                    # Forming content of request
                    data = ApiCallData({
                        'code': code,
                        'compiler': compiler,
                        'stdin': current_test.test_input
                    })

                    # Creating asyncio task
                    asyncio_task = asyncio.ensure_future(self.__run_single_test(session, data, current_test))
                    tasks.append(asyncio_task)

                test_results = await asyncio.gather(*tasks)  # Running tasks

                end_time = time.time()

                # Results of testing
                tests = sorted(test_results, key=lambda item: item.success)
                return ContesterResponse(
                    language=current_language,
                    tests=tests,
                    passed_tests=get_number_of_passed_tests(tests),
                    time="{0:.3f} sec".format(end_time - start_time)
                )
        return None

    @silence_event_loop_closed
    def run_tests(
            self,
            code: str,
            language: str,
            task: Task,
            partner: t.Optional[User] = None
    ) -> dict:
        """
        :param code: User's code
        :param language: Programming language
        :param task: Task object
        :param partner: User object (person who helped to write solution)
        :return: Dictionary with the results of testing the program
        """

        loop = asyncio.new_event_loop()  # Creating async loop
        response = loop.run_until_complete(self.__get_testing_results(code, language, task))

        # Saving results to DB
        # if not self.TESTING_MODE:
        #     self.__save_to_database(task=task, code=code, response=response, language=language, partner=partner)
        # Printing response
        if app.config.get('TESTING'):
            pprint.pprint(response, indent=4)

        return response


contester = Contester()
