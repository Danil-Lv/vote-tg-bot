from aiogram import types, Dispatcher

from .handling_post import PostStateGroup
from keyboards import kb_start


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text='Бот для создания опросов. Создать опрос - /create', reply_markup=kb_start)


# @dp.message_handler(commands=['create'])
async def create(message: types.Message):
    await message.answer(text='Перешли сюда последнее сообщение из канала')
    await PostStateGroup.last_post.set()



def commands_handlers_register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(create, commands=['create'])
