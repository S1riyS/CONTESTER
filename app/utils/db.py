from app import db
from app.models import Grade, Topic, Task


def get_task(grade_number, topic_translit_name, task_translit_name):
    return db.session.query(Task).filter(
        Grade.number == grade_number,
        Topic.translit_name == topic_translit_name,
        Task.translit_name == task_translit_name
    ).first()
