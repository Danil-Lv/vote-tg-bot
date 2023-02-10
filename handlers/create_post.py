from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import logging

from create_bot import bot
from keyboards import kb_create_post, ikb_public

from db.db_commands import add_answer, get_answer, add_question, delete_post


class PostStateGroup(StatesGroup):
    question = State()
    ans1 = State()
    ans1_desc = State()
    ans2 = State()
    ans2_desc = State()
    ans3 = State()
    ans3_desc = State()
    ans4 = State()
    ans4_desc = State()
    photo = State()
    send = State()


# @dp.message_handler(state='*', text='Прекратить создание поста')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(state=PostStateGroup.question)
async def question(message: types.Message, state):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer('Напиши вариант ответа 1', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b1)
async def ans1(message: types.Message, state):
    async with state.proxy() as data:
        data['ans1'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b1_desc)
async def ans1_desc(message: types.Message, state):
    async with state.proxy() as data:
        data['ans1_desc'] = message.text

    await message.answer('Напиши 2 вариант ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b2)
async def ans2(message: types.Message, state):
    async with state.proxy() as data:
        data['ans2'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b2_desc)
async def ans2_desc(message: types.Message, state):
    async with state.proxy() as data:
        data['ans2_desc'] = message.text

    await message.answer('Напиши 3 вариант ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b3)
async def ans3(message: types.Message, state):
    async with state.proxy() as data:
        data['ans3'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b3_desc)
async def ans3_desc(message: types.Message, state):
    async with state.proxy() as data:
        data['ans3_desc'] = message.text

    await message.answer('Напиши 4 вариант ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b4)
async def ans4(message: types.Message, state):
    async with state.proxy() as data:
        data['ans4'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)
    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b4_desc)
async def ans4_desc(message: types.Message, state):
    async with state.proxy() as data:
        data['ans4_desc'] = message.text

    await message.answer('Теперь пришли фотографию', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(content_types=['photo'], state=PostStateGroup.photo)
async def photo(message: types.Message, state):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await show_post(message, state)
    await state.finish()


# @dp.message_handler()
async def show_post(message: types.Message, state):
    global ikb
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        ikb = InlineKeyboardMarkup(row_width=2)
        ans1_btn = InlineKeyboardButton(text=f'{data["ans1"]}', callback_data='vote1')
        ans2_btn = InlineKeyboardButton(text=f'{data["ans2"]}', callback_data='vote2')
        ans3_btn = InlineKeyboardButton(text=f'{data["ans3"]}', callback_data='vote3')
        ans4_btn = InlineKeyboardButton(text=f'{data["ans4"]}', callback_data='vote4')

        ikb.add(ans1_btn, ans2_btn, ans3_btn, ans4_btn)

        new_question = await add_question(title=data['question'])
        for i in range(1, 5):
            await add_answer(caption_id=new_question.id, title=data[f'ans{i}'], description=data[f'ans{i}_desc'])

        await message.answer(text='Твой пост выглядит так:')

        await bot.send_photo(photo=data['photo'],
                             chat_id=message.from_user.id,
                             caption=data['question'],
                             reply_markup=ikb)

        call_back_info = CallbackData('Здесь префикс объекта', 'data')

    await message.answer(text='Опубликовать?', reply_markup=ikb_public)


# @dp.callback_query_handler(lambda x: x.data.startswith('public'))
async def public(callback: types.CallbackQuery, state):
    async with state.proxy() as data:
        if callback.data.split('_')[-1] == 'not':
            await delete_post(question=data['question'])
            await callback.message.delete()
            await callback.message.answer('Пост удален. Создать новый - /create')
        else:
            await bot.send_photo(photo=data['photo'],
                                 chat_id=-1001612936953,
                                 caption=data['question'],
                                 reply_markup=ikb)

            await callback.message.answer('Пост опубликован')


# @dp.callback_query_handler(lambda x: x.data.startswith('vote'))
async def vote(callback: types.CallbackQuery):
    button = callback.data[-1]
    if button == '1':
        title = callback.message.reply_markup.values['inline_keyboard'][0][0].text
    elif button == '2':
        title = callback.message.reply_markup.values['inline_keyboard'][0][1].text
    elif button == '3':
        title = callback.message.reply_markup.values['inline_keyboard'][1][0].text
    elif button == '4':
        title = callback.message.reply_markup.values['inline_keyboard'][1][1].text

    res = await get_answer(callback.message.caption, title)
    await callback.answer(res.description, show_alert=True)


def create_handlers_register(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', text='Прекратить создание поста')
    dp.register_message_handler(question, state=PostStateGroup.question)
    dp.register_message_handler(ans1, state=PostStateGroup.ans1)
    dp.register_message_handler(ans1_desc, state=PostStateGroup.ans1_desc)
    dp.register_message_handler(ans2, state=PostStateGroup.ans2)
    dp.register_message_handler(ans2_desc, state=PostStateGroup.ans2_desc)
    dp.register_message_handler(ans3, state=PostStateGroup.ans3)
    dp.register_message_handler(ans3_desc, state=PostStateGroup.ans3_desc)
    dp.register_message_handler(ans4, state=PostStateGroup.ans4)
    dp.register_message_handler(ans4_desc, state=PostStateGroup.ans4_desc)
    dp.register_message_handler(photo, content_types=['photo'], state=PostStateGroup.photo)
    dp.register_callback_query_handler(public, lambda x: x.data.startswith('public'))
    dp.register_callback_query_handler(vote, lambda x: x.data.startswith('vote'))
