import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(100), unique=True, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.Text, default='')
    hashed_password = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    films = orm.relationship("Film", back_populates='user')
    reviews = orm.relationship("Review", back_populates='user')
    comments = orm.relationship("Comment", back_populates='user')
    forum_posts = orm.relationship("ForumPost", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)