import typing as t
import platform
from functools import wraps

from asyncio.proactor_events import _ProactorBasePipeTransport

from .types import SingleTestResult


def get_number_of_passed_tests(tests: t.Iterable[SingleTestResult]) -> int:
    return len([result for result in tests if result.success])


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


if platform.system() == 'Windows':
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
