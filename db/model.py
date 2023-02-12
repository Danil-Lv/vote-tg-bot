from sqlalchemy import Column, sql
from .database import db


class Answer(db.Model):
    """Вариант ответа"""
    __tablename__ = 'answers'

    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50))
    description = Column(db.String(200))
    position = Column(db.Integer)
    count = Column(db.Integer, default=0)

    question_id = Column(db.ForeignKey('questions.id'))


class Question(db.Model):
    """Вопрос"""

    __tablename__ = 'questions'
    id = Column(db.Integer, primary_key=True)
    message_id = Column(db.BigInteger)
    promo = Column(db.Boolean)
    count = Column(db.Integer, default=0) # total_count


class UserQuestion(db.Model):
    """id последнего сообщения в канале"""

    __tablename__ = 'user_questions'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.BigInteger)
    question_id = Column(db.ForeignKey('questions.id'))


class LastId(db.Model):
    """id последнего сообщения в канале"""

    __tablename__ = 'last_id'

    query: sql.Select
    id = Column(db.Integer, primary_key=True)
    last_id = Column(db.Integer)
