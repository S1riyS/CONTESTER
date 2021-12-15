# import requests
# from typing import Optional
# import pprint
#
# from .errors import ServerResponseException, ExecutionException
#
# languages = {
#     'cpp': {
#         'name': 'C++',
#         'compiler': 'gcc-head',
#         'mode': 'text/x-c++src'},
#     'csharp': {
#         'name': 'C#',
#         'compiler': 'mono-head',
#         'mode': 'text/x-csharp'},
#     'java': {
#         'name': 'Java',
#         'compiler': 'openjdk-head',
#         'mode': 'text/x-java'},
#     'python': {
#         'name': 'Python 3',
#         'compiler': 'cpython-head',
#         'mode': 'text/x-python',
#         'is_default': True},
#     'pascal': {
#         'name': 'Pascal',
#         'compiler': 'fpc-head',
#         'mode': 'text/x-pascal'},
# }
#
#
# class Contester:
#     def __init__(self):
#         self.WANDBOX_COMPILE_URL = 'https://wandbox.org/api/compile.json'
#         self.DEFAULT_TIMEOUT = 2.75
#         self.HEADERS = {
#             'Content-Type': "application/json;charset=UTF-8",
#         }
#
#     def _send_wandbox_request(self, content: dict) -> requests.models.Response:
#         print(content)
#         # Sending request to WandBox
#         return requests.post(url=self.WANDBOX_COMPILE_URL,
#                              json=content,
#                              headers=self.HEADERS,
#                              timeout=self.DEFAULT_TIMEOUT)
#
#     @staticmethod
#     def _compare_answers(program_output: str, expected_output: str) -> Optional[AssertionError]:
#         assert program_output.strip() == expected_output.strip()  # Checking answer
#
#     def run_tests(self, code_value: str, language: str, tests: list) -> dict:
#         is_tab_to_show = False
#         response = {'tests': {}}  # Base of response
#         compiler = languages[language]['compiler']  # Getting compiler
#
#         for index, current_test in enumerate(tests):
#             try:
#                 print(current_test)
#                 test_number = index + 1  # Calculating current test number
#
#                 # Forming content of request
#                 data = {
#                     'code': code_value,
#                     'compiler': compiler,
#                     'stdin': current_test['stdin']
#                 }
#
#                 # Sending request to WandBox
#                 wandbox_response = self._send_wandbox_request(content=data)
#
#                 # Checking status code
#                 if wandbox_response.status_code != 200:
#                     raise ServerResponseException  # Raising 'ServerResponseException'
#
#                 else:
#                     # Getting JSON
#                     result_json = wandbox_response.json()  # JSON
#
#                     # Checking status
#                     if result_json['status'] == '0':
#                         self._compare_answers(program_output=result_json['program_output'],
#                                               expected_output=current_test['output'])
#
#                         # If everything OK
#                         test_result = {'status': 'OK', 'message': 'Success'}
#                         print(f'Passed test number {test_number}')
#
#                     else:
#                         raise ExecutionException  # Raising 'ExecutionException'
#
#             # Exceptions block
#             except ServerResponseException:
#                 test_result = {'status': 'ERROR', 'message': 'Server Response Error'}
#                 print(f'Failed test number {test_number}, Server Response Error')
#
#             except ExecutionException:
#                 test_result = {'status': 'ERROR', 'message': 'Execution Error'}
#                 print(f'Failed test number {test_number}, Execution Error')
#
#             except requests.Timeout:
#                 test_result = {'status': 'ERROR', 'message': 'Timeout Error'}
#                 print(f'Failed test number {test_number}, Timeout Error')
#
#             except AssertionError:
#                 test_result = {'status': 'ERROR', 'message': 'Wrong Answer'}
#                 print(f'Failed test number {test_number}, Wrong Answer')
#
#             finally:
#                 # Checking structure of result
#                 if test_result['status'] and test_result['message']:
#                     pass
#                 else:
#                     test_result = {'status': 'ERROR', 'message': 'Testing System Error'}
#
#                 # Checking if test can be shown
#                 if not current_test['hidden']:
#                     test_result['info'] = {
#                         'stdin': current_test['stdin'],
#                         'expected-output': current_test['output']
#                     }
#                     if not is_tab_to_show:
#                         test_result['to_show'] = True
#                         is_tab_to_show = True
#                 else:
#                     test_result['info'] = None
#
#                 response['tests'][test_number] = test_result  # Writing result to response dictionary
#
#         # Calculating total number of passed tests
#         passed_tests = len([result for result in response['tests'].values() if result['status'] == 'OK'])
#         response['passed_tests'] = passed_tests
#
#         pprint.pprint(response, width=1)
#         return response
#
#     @staticmethod
#     def get_tests(task: dict) -> dict:
#         tests = [
#             {
#                 'stdin': '1 2',
#                 'output': '3',
#                 'hidden': False
#             },
#             {
#                 'stdin': '1 5',
#                 'output': '6',
#                 'hidden': False
#             },
#             {
#                 'stdin': '2 5',
#                 'output': '7',
#                 'hidden': True
#             },
#             {
#                 'stdin': '5 6',
#                 'output': '11',
#                 'hidden': True
#             }
#         ]
#
#         return tests

from typing import Optional
import pprint

import asyncio
import aiohttp

from .errors import ServerResponseError, ExecutionError

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
        self.COMPILER_URL = 'https://wandbox.org/api/compile.json'  # Compiler URL
        self.AIOHTTP_TIMEOUT = aiohttp.ClientTimeout(total=2.5)  # Timeout value
        # Request headers
        self.HEADERS = {
            'Content-Type': "application/json;charset=UTF-8",
        }
        # Dictionary with programming languages (name, compiler, CodeMirror mode)
        self.LANGUAGES = {
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

    @staticmethod
    def _get_compiler(language) -> str:
        return languages[language]['compiler']

    @staticmethod
    def _compare_answers(program_output, expected_output) -> Optional[AssertionError]:
        assert program_output.strip() == expected_output.strip()  # Checking answer

    @staticmethod
    def _get_number_of_passed_tests(tests):
        return len([result for result in tests.values() if result['status'] == 'OK'])

    async def _run_test(self, session, data, current_test, test_number) -> dict:
        """
        :param session: aiohttp.ClientSession() object
        :param data: params which will be passed in the request
        :param test_number: Number of test
        :return: Dictionary with result of test
        """
        response = {}
        result = {'status': None, 'message': None}

        try:
            async with session.post(url=self.COMPILER_URL, headers=self.HEADERS, json=data) as wandbox_response:
                # Checking status code
                if wandbox_response.status != 200:
                    raise ServerResponseException  # Raising 'ServerResponseException'
                else:
                    result_json = await wandbox_response.json()  # Getting JSON

                    # Checking status
                    if result_json['status'] == '0':
                        self._compare_answers(program_output=result_json['program_output'],
                                              expected_output=current_test['output'])

                        # If everything OK
                        result = {'status': 'OK', 'message': 'Success'}
                        print(f'Passed test number {test_number}')

                    else:
                        raise ExecutionException  # Raising 'ExecutionException'

        # Exceptions block
        except ServerResponseError:
            result = {'status': 'ERROR', 'message': 'Server Response Error'}
            print(f'Failed test number {test_number}, Server Response Error')

        except ExecutionError:
            result = {'status': 'ERROR', 'message': 'Execution Error'}
            print(f'Failed test number {test_number}, Execution Error')

        except asyncio.TimeoutError:
            result = {'status': 'ERROR', 'message': 'Timeout Error'}
            print(f'Failed test number {test_number}, Timeout Error')

        except AssertionError:
            result = {'status': 'ERROR', 'message': 'Wrong Answer'}
            print(f'Failed test number {test_number}, Wrong Answer')

        finally:
            # Checking structure of result
            if not (result['status'] and result['message']):
                result = {'status': 'ERROR', 'message': 'Testing System Error'}

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
        response = {'tests': {}}  # Base of response
        compiler = self._get_compiler(language)  # Getting compiler

        async with aiohttp.ClientSession(timeout=self.AIOHTTP_TIMEOUT) as session:
            tasks = []

            for index, current_test in enumerate(tests):
                # Forming content of request
                data = {
                    'code': code,
                    'compiler': compiler,
                    'stdin': current_test['stdin']
                }

                # Getting current test
                test = tests[index]

                # Creating asyncio task
                task = asyncio.ensure_future(self._run_test(session, data, test, index))
                tasks.append(task)

            test_results = await asyncio.gather(*tasks)  # Running tasks

            # Writing sub-dictionary with results of testing to response
            for test_result in test_results:
                test_number = test_result['test_number'] + 1
                response['tests'][test_number] = test_result['result']

            # Calculating total number of passed tests
            response['passed_tests'] = self._get_number_of_passed_tests(response['tests'])

            return response

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
    def get_tests(task=None):
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

