from aiogram import types, Dispatcher
from aiogram.dispatcher.webhook import SendMessage

from .create_post import check_id
from .handling_post import PostStateGroup
from keyboards import kb_create_post


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('hello')
    await check_id.set()
    return SendMessage(message.chat.id, 'Бот для создания опросов. Пришли мне последнее созданное сообщение из канала')


# @dp.message_handler(commands=['create'])
async def create(message: types.Message):
    await message.answer(text='Напиши вопрос')
    await message.answer(text='Если хочешь создать пост без вопроса напиши -', reply_markup=kb_create_post)
    await PostStateGroup.question.set()


def commands_handlers_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(create, commands=['create'])
