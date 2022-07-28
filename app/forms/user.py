from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    surname = StringField('Имя', validators=[DataRequired()])
    name = StringField('Фамилия', validators=[DataRequired()])
    grade_id = SelectField('Класс', choices=[], validators=[DataRequired()])
    grade_letter = SelectField('Буква', choices=['А', 'Б', 'В', 'Г'], validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
