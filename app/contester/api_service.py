import typing as t
from dataclasses import dataclass, field

import asyncio
from aiohttp import ClientSession
from .exceptions import ContesterError, ApiServiceError, ExecutionError, WrongAnswerError, TimeOutError

API_URL = 'https://wandbox.org/api/compile.json'  # API URL
HEADERS = {'Content-Type': "application/json;charset=UTF-8"}  # Request headers


class ApiCallParameters(t.TypedDict):
    code: str
    compiler: str
    stdin: str


class ParsedApiResponse(t.NamedTuple):
    success: bool
    message: str
    user_output: t.Optional[str]


@dataclass
class ApiCall:
    __session: ClientSession
    __data: ApiCallParameters
    __expected_output: str
    __user_output: t.Optional[str] = field(init=False, default=None)

    @staticmethod
    def __compare_answers(user_output: str, expected_output: str) -> bool:
        """Compares user's answer and expected answer"""
        if user_output.strip() == expected_output.strip():
            return True
        return False

    async def __get_api_response(self) -> t.Optional[t.Any]:
        """Requests code compilation in Wandbox and returns JSON with results

        Raises
        ------
        ApiServiceError
            If can't get valid response from API service
        TimeOutError
            If the request has exceeded the maximum allowed time
        """
        try:
            async with self.__session.post(url=API_URL, headers=HEADERS, json=self.__data, timeout=10) as api_response:
                if api_response.status == 200:
                    response_json = await api_response.json()
                    return response_json
                raise ApiServiceError
        except asyncio.TimeoutError:
            raise TimeOutError

    def __process_response(self, response: t.Any) -> None:
        """Processes API response by checking the response status and comparing the expected output with user's

        Raises
        ------
        ExecutionError
            If the API service failed to run user's code
        WrongAnswerError
            If user's output doesn't match expected output
        """
        if response['status'] == '0':
            self.__user_output = response['program_output'].strip()
            if self.__compare_answers(self.__user_output, self.__expected_output):
                return
            raise WrongAnswerError
        raise ExecutionError

    async def run(self):
        """Sends API call and processes response"""
        response = await self.__get_api_response()
        self.__process_response(response)

    @property
    def user_output(self):
        return self.__user_output


async def parse_api_call(call: ApiCall) -> ParsedApiResponse:
    try:
        await call.run()

    except ContesterError as error:
        success = False
        message = error.message

    else:
        success = True
        message = 'Success'

    return ParsedApiResponse(
        success=success,
        message=message,
        user_output=call.user_output
    )
