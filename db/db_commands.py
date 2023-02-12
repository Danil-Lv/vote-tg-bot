from sqlalchemy import and_

from db.model import *

"""Last id"""


async def create_last_message_id(**kwargs):
    new_id = await LastId(**kwargs).create()
    return new_id


async def get_last_message_id():
    last_message_id = await LastId.query.gino.first()
    return last_message_id


async def update_last_message_id(id_new=None):  # Нужени ли id_new?
    last_message_id = await LastId.query.gino.first()
    if id_new:
        await last_message_id.update(last_id=id_new).apply()
    else:
        await last_message_id.update(last_id=last_message_id.last_id + 1).apply()



#     прописать в хендлере если None то требуем пост создаем айди


"""Вопрос"""


async def create_question(**kwargs):
    new_question = await Question(**kwargs).create()
    return new_question


async def get_question(message_id):
    question = await Question.query.where(Question.message_id == message_id).gino.first()

    return question


async def delete_question(message_id):
    question = await get_question(message_id)
    for i in range(4):
        await Answer.delete.where(Answer.question_id == question.id).gino.status()
    await UserQuestion.delete.where(UserQuestion.question_id == question.id).gino.status()
    await Question.delete.where(Question.message_id == message_id).gino.status()



"""Answer"""


async def create_answer(**kwargs):
    newanswer = await Answer(**kwargs).create()
    return newanswer


async def get_answer(question_id, position):
    answer = await Answer.query.where(
        and_(Answer.question_id == question_id,
             Answer.position == position)
    ).gino.first()

    return answer

async def post_counter_increase(answer_id, question_id):
    question = await Question.query.where(Question.id == question_id).gino.first()
    answer = await Answer.query.where(Answer.id == answer_id).gino.first()
    await answer.update(count=answer.count + 1).apply()
    await question.update(count=question.count + 1).apply()




"""User_Question"""


async def create_user_question(**kwargs):
    new_user_question = await UserQuestion(**kwargs).create()
    return new_user_question


async def get_user_question(user_id, question_id):
    user_question = await UserQuestion.query.where(
        and_(UserQuestion.user_id == user_id,
             UserQuestion.question_id == question_id)
    ).gino.first()

    return user_question

"""Получение результата ответов"""

async def get_results(question_id):
    answers = await Answer.query.where(Answer.question_id == question_id).gino.all()

    return answers
