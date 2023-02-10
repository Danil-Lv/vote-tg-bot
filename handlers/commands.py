from aiogram import types, Dispatcher

from .create_post import PostStateGroup
from keyboards import kb_start, kb_create_post


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text='Бот для создания опросов. Создать опрос - /create', reply_markup=kb_start)


# @dp.message_handler(commands=['create'])
async def create(message: types.Message):
    await message.answer(text='Напиши вопрос', reply_markup=kb_create_post)
    await PostStateGroup.question.set()


def commands_handlers_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(create, commands=['create'])