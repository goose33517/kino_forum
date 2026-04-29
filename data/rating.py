import sqlalchemy
from .db_session import SqlAlchemyBase

class Rating(SqlAlchemyBase):
    __tablename__ = 'ratings'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    film_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))