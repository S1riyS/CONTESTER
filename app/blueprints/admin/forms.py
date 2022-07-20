from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):
    grade = SelectField('Класс', choices=[], validators=[DataRequired()])
    topic_name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Создать тему')


class TaskForm(FlaskForm):
    grade = SelectField('Класс', choices=[], validators=[DataRequired()])
    topic = SelectField('Тема', choices=[], validators=[DataRequired()])
    task_name = StringField('Название', validators=[DataRequired()])
    condition = TextAreaField('Условие', validators=[DataRequired()])
    example_stdin = TextAreaField('Условие', validators=[DataRequired()])
    example_stdout = TextAreaField('Условие', validators=[DataRequired()])
    submit = SubmitField('Создать задачу')
