from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    stdin = TextAreaField('Ввод', validators=[DataRequired()])
    stdout = TextAreaField('Вывод', validators=[DataRequired()])
    is_hidden = BooleanField('Скрыть', default=True)


class TopicForm(FlaskForm):
    grade_id = SelectField('Класс', choices=[], validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField()


class TaskForm(FlaskForm):
    grade_id = SelectField('Класс', choices=[], validators=[DataRequired()])
    topic_id = SelectField('Тема', choices=[], validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    condition = TextAreaField('Условие', validators=[DataRequired()])
    example_stdin = TextAreaField('Ввод', validators=[DataRequired()])
    example_stdout = TextAreaField('Вывод', validators=[DataRequired()])
    tests = FieldList(FormField(TestForm), min_entries=1)
    submit = SubmitField('Создать задачу')
