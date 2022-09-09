from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    surname = StringField('Имя', validators=[DataRequired()])
    name = StringField('Фамилия', validators=[DataRequired()])
    grade_id = SelectField('Класс', choices=[], validate_choice=False)
    grade_letter = SelectField('Буква', choices=['А', 'Б', 'В', 'Г'], validate_choice=False)
    is_admin = BooleanField('Права администратора', default=False)
    submit = SubmitField('Отправить')
