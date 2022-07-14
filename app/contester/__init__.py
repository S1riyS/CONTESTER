import typing as t
from dataclasses import dataclass
import time
import pprint

import asyncio
from aiohttp import ClientSession

from app import app
from app.models import User, Task, Test

from .api_service import ApiCall, ApiCallData
from .languages import Language, languages
from .db_manager import save_to_database
from .utils import get_number_of_passed_tests, silence_event_loop_closed
from .types import SingleTestResult, ContesterResponse
from .exceptions import ContesterError


@dataclass
class Contester:
    TESTING_MODE: bool = False

    @staticmethod
    async def __run_single_test(session: ClientSession, data: ApiCallData, test: Test) -> SingleTestResult:
        """Returns result of a single test"""
        try:
            api_call = ApiCall(session, data, test.stdout)
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
            test=test,
            user_output=user_output
        )

    async def __get_testing_results(self, code: str, language: str, task: Task) -> ContesterResponse:
        """Asynchronously runs all tests and returns `ContesterResponse` object"""
        current_language_dict = languages.get_language(language)

        if current_language_dict['success']:
            current_language = current_language_dict['language']
            compiler = current_language.compiler
            start_time = time.time()

            async with ClientSession() as session:
                tasks = []

                for test in task.tests:
                    # Forming content of request
                    data = ApiCallData({
                        'code': code,
                        'compiler': compiler,
                        'stdin': test.stdin
                    })

                    # Creating asyncio task
                    asyncio_task = asyncio.ensure_future(self.__run_single_test(session, data, test))
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
    ) -> ContesterResponse:
        """Returns results of testing"""

        loop = asyncio.new_event_loop()  # Creating async loop
        response = loop.run_until_complete(self.__get_testing_results(code, language, task))

        # Saving results to DB
        if not self.TESTING_MODE:
            save_to_database(task=task, code=code, response=response, language=language, partner=partner)
        # Printing response
        if app.config.get('TESTING'):
            pprint.pprint(response, indent=4)

        return response


contester = Contester()
