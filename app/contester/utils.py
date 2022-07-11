import typing as t

from .types import SingleTestResult

def get_number_of_passed_tests(tests: t.Iterable[SingleTestResult]) -> int:
    return len([result for result in tests if result.success])
