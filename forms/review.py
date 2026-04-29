from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange

class ReviewForm(FlaskForm):
    title = StringField('Заголовок рецензии', validators=[DataRequired()])
    content = TextAreaField('Текст рецензии', validators=[DataRequired()])
    rating = IntegerField('Оценка (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Опубликовать')