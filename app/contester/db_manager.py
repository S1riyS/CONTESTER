import typing as t

from flask_login import current_user

from app import db
from app.models import User, Task, Submission, TestResult
from .languages import languages
from .types import ContesterResponse, SingleTestResult
from .utils import get_number_of_passed_tests


def save_to_database(
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


def load_from_database(submission: Submission) -> ContesterResponse:
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
