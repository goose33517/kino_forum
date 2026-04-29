from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired

class LoginForms(FlaskForm):
    naiti = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Найти')