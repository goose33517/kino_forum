import sqlalchemy
from .db_session import SqlAlchemyBase

class Favorite(SqlAlchemyBase):
    __tablename__ = 'favorites'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    film_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("films.id"))