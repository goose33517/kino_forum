from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField, BooleanField
from wtforms.validators import DataRequired

class HelloForm(FlaskForm):
    movie = StringField('Ваш любимый фильм', validators=[DataRequired()])
    rating = IntegerField('Оцените фильм')
    review = StringField('Ваш отзыв')
    agree = BooleanField('Согласен на обработку данных', validators=[DataRequired()])
    submit = SubmitField('Отправить отзыв')
