import typing as t

from app.models import Test

from .languages import Language


class SingleTestResult(t.NamedTuple):
    message: str
    success: bool
    test: Test
    user_output: str


class ContesterResponse(t.NamedTuple):
    language: Language
    tests: t.Iterable[SingleTestResult]
    passed_tests: int
    time: str
