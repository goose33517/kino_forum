import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Film(SqlAlchemyBase):
    __tablename__ = 'films'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)
    director = sqlalchemy.Column(sqlalchemy.String(200))
    year = sqlalchemy.Column(sqlalchemy.Integer)
    genre = sqlalchemy.Column(sqlalchemy.String(500))
    country = sqlalchemy.Column(sqlalchemy.String(200))
    duration = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.Text)
    rating = sqlalchemy.Column(sqlalchemy.Float, default=0.0)
    review_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User", back_populates='films')
    reviews = orm.relationship("Review", back_populates='film')