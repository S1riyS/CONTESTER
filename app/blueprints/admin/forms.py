from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class TopicForm(FlaskForm):
    grade = SelectField('Класс', choices=[], validators=[DataRequired()])
    topic_name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Создать тему')
