from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class NewThreadForm(FlaskForm):
    title = StringField('Название треда: ', validators=[DataRequired()])
    message = TextAreaField('Сообщение: ', validators=[DataRequired()])

class NewPostForm(FlaskForm):
    message = TextAreaField('Сообщение: ', validators=[DataRequired()])

class LogRegForm(FlaskForm):
    username = StringField('Имя пользователя: ', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
