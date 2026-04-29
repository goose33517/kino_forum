from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
from config import GENRES, COUNTRIES, YEARS

class FilmForm(FlaskForm):
    title = StringField('Название фильма', validators=[DataRequired()])
    director = StringField('Режиссер', validators=[DataRequired()])
    year = SelectField('Год', choices=[(y, y) for y in YEARS], coerce=int)
    genre = SelectField('Жанр', choices=[(g, g) for g in GENRES])
    country = SelectField('Страна', choices=[(c, c) for c in COUNTRIES])
    duration = IntegerField('Длительность (мин)')
    description = TextAreaField('Описание')
    submit = SubmitField('Добавить фильм')