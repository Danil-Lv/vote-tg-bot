from sqlalchemy import and_

from .model import Answer, Question


async def add_question(**kwargs):
    newquestion = await Question(**kwargs).create()
    return newquestion


async def get_question(caption):
    question = await Question.query.where(Question.title == caption).gino.first()
    return question


async def add_answer(**kwargs):
    newanswer = await Answer(**kwargs).create()
    return newanswer


async def get_answer(caption, title):
    question = await get_question(caption)
    answer = await Answer.query.where(
        and_(Answer.caption_id == question.id,
             Answer.title == title)
    ).gino.first()

    return answer


async def delete_post(question):
    question = await get_question(question)
    await Question.delete.where(Question.id == question.id).gino.status()
    for i in range(4):
        await Answer.delete.where(Answer.caption_id == question.id).gino.status()
