from sqlalchemy import Column, sql, Sequence
from .database import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(100))


class Answer(db.Model):
    __tablename__ = 'answers'

    query: sql.Select

    id = Column(db.Integer, primary_key=True)

    caption_id = Column(db.Integer)

    title = Column(db.String(20))
    description = Column(db.String(200))
    count = Column(db.Integer, default=0)
