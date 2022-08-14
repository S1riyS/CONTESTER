import typing as t
from dataclasses import dataclass
import time
import pprint

from flask import current_app as app
import asyncio
from aiohttp import ClientSession

from app.models import User, Task, Test

from .api_service import ApiCall, ApiCallParameters, parse_api_call
from .languages import Language, languages
from .db_manager import save_to_database
from .utils import get_number_of_passed_tests, silence_event_loop_closed
from .types import SingleTestResult, ContesterResponse

try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except AttributeError:
    print('Cannot set asyncio WindowsSelectorEventLoopPolicy')


@dataclass
class Contester:
    TESTING_MODE: bool = False

    @staticmethod
    async def __run_single_test(session: ClientSession, data: ApiCallParameters, test: Test) -> SingleTestResult:
        """Returns result of a single test"""
        api_call = ApiCall(session, data, test.stdout)
        response = await parse_api_call(api_call)

        return SingleTestResult(
            test=test,
            message=response.message,
            success=response.success,
            user_output=response.user_output
        )

    def __collect_asyncio_tasks(
            self,
            session: ClientSession,
            task: Task,
            code: str,
            compiler: str
    ) -> t.Iterable[asyncio.Task]:
        """Returns list of asyncio.Task"""
        tasks = []

        for test in task.tests:
            # Forming content of request
            data = ApiCallParameters({
                'code': code,
                'compiler': compiler,
                'stdin': test.stdin
            })

            # Creating asyncio task
            asyncio_task = asyncio.ensure_future(self.__run_single_test(session, data, test))
            tasks.append(asyncio_task)

        return tasks

    async def __get_testing_results(self, code: str, language: str, task: Task) -> ContesterResponse:
        """Asynchronously runs all tests and returns `ContesterResponse` object"""
        current_language_dict = languages.get_language(language)

        if not current_language_dict['success']:
            return None  # language not found

        # Getting compiler
        current_language = current_language_dict['language']
        compiler = current_language.compiler

        # Running tests
        start_time = time.time()
        async with ClientSession() as session:
            tasks = self.__collect_asyncio_tasks(session, task, code, compiler)
            test_results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Results of testing
        tests = sorted(test_results, key=lambda item: item.success)
        passed_tests = get_number_of_passed_tests(tests)
        execution_time = "{0:.3f} sec".format(end_time - start_time)

        return ContesterResponse(
            language=current_language,
            tests=tests,
            passed_tests=passed_tests,
            time=execution_time
        )

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
        if app.config.get('TESTING') and not self.TESTING_MODE:
            pprint.pprint(response, indent=4)

        return response


contester = Contester()
