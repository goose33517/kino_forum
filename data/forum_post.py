import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class ForumPost(SqlAlchemyBase):
    __tablename__ = 'forum_posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String(100))
    views = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    comment_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User", back_populates='forum_posts')
    comments = orm.relationship("Comment", back_populates='forum_post')