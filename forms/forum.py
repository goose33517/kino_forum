from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ForumPostForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired()])
    content = TextAreaField('Сообщение', validators=[DataRequired()])
    category = SelectField('Раздел', choices=[
        ('Обсуждение фильмов', 'Обсуждение фильмов'),
        ('Новости кино', 'Новости кино'),
        ('Советы', 'Советы'),
        ('Сериалы', 'Сериалы'),
        ('Оффтоп', 'Оффтоп')
    ])
    submit = SubmitField('Создать тему')