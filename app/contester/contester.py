import requests

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

    def run_tests(self, code_value: str, language: str, tests: dict) -> dict:
        response = {'tests': {}}

        headers = {
            'Content-Type': "application/json;charset=UTF-8",
        }
        compiler = languages[language]['compiler']
        for index, (input_value, output_value) in enumerate(tests.items()):
            try:
                data = {
                    'code': code_value,
                    'compiler': compiler,
                    'stdin': input_value
                }

                result = requests.post(url=self.WANDBOX_COMPILE_URL, json=data, headers=headers)

                if result.status_code != 200:
                    answer = None
                else:
                    result_json = result.json()
                    if 'program_message' in result_json:
                        answer = result_json['program_message'].strip()
                    else:
                        print(result_json)
                        answer = None

                print(answer, output_value)

                assert answer == output_value

                print(f'Passed test number {index}')
                response['tests'][index + 1] = True

            except AssertionError:
                print(f'Failed test number {index}, incorrect answer')
                response['tests'][index + 1] = False

        passed_tests = len([result for result in response['tests'].values() if result])
        response['passed_tests'] = passed_tests

        return response

    @staticmethod
    def get_tests(task: dict) -> dict:
        return {
            '1 2': '3',
            '1 5': '6',
            '2 5': '7',
            '5 6': '11',
        }
