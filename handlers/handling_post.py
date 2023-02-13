from os import getenv

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from create_bot import bot
from handlers.commands import check_id
from keyboards import kb_create_post, ikb_public, kb_statistic, kb_question, kb_start
from handlers.create_post import PostStateGroup
from db.db_commands import *


# @dp.channel_post_handler(content_types=[types.ContentType.ANY])
async def get_any_post(message: types.Message):
    """Обработка всех сообщений приходящих в канал"""
    await update_last_message_id(message.message_id)


async def keyboard_type(message: types.Message, state):
    """Выбор типа клавиатуры"""
    async with state.proxy() as data:
        if message.text == 'Большая':
            data['kb_type'] = 'big'
        elif message.text == 'Компактная':
            data['kb_type'] = 'small'
        elif message.text == 'В строку':
            data['kb_type'] = 'one_row'
        await message.answer('Добавить кнопку статистики?', reply_markup=kb_question)

        await PostStateGroup.next()


async def add_statistics(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Да':
            data['kb_statistics'] = True
            await message.answer('Введи текст для кнопки статистики', reply_markup=kb_statistic)
            await PostStateGroup.next()
        elif message.text == 'Нет':
            data['kb_statistics'] = False
            await show_post(message, state, kb_stat=False)


async def add_statistics_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['kb_statistics_text'] = message.text

    await show_post(message, state, kb_stat=True)


# @dp.message_handler()
async def show_post(message: types.Message, state: FSMContext, kb_stat):
    """Вывод сообщения при модерации"""
    global data
    async with state.proxy() as data:
        if data['kb_type'] == 'big':
            rows = 1
        elif data['kb_type'] == 'small':
            rows = 2
        elif data['kb_type'] == 'one_row':
            rows = 4

        ikb = InlineKeyboardMarkup(row_width=rows)
        ans1_btn = InlineKeyboardButton(text=f'{data["ans1"]}', callback_data='vote1')
        ans2_btn = InlineKeyboardButton(text=f'{data["ans2"]}', callback_data='vote2')
        ans3_btn = InlineKeyboardButton(text=f'{data["ans3"]}', callback_data='vote3')
        ans4_btn = InlineKeyboardButton(text=f'{data["ans4"]}', callback_data='vote4')

        ikb.add(ans1_btn, ans2_btn, ans3_btn, ans4_btn)

        if kb_stat:
            show_results_btn = InlineKeyboardButton(text=data['kb_statistics_text'], callback_data='show_results')
            ikb.insert(show_results_btn)
        data['ikb'] = ikb

        last_message_id = await get_last_message_id()
        question = await create_question(message_id=last_message_id.last_id + 1, promo=data['promo'])

        for i in range(1, 5):
            await create_answer(question_id=question.id, title=data[f'ans{i}'], description=data[f'ans{i}_desc'],
                                position=i)

        await message.answer(text='Твой пост выглядит так:')

        if data['question'] == '-':
            await bot.send_photo(photo=data['photo'],
                                 chat_id=message.from_user.id,
                                 reply_markup=ikb)
        else:
            await bot.send_photo(photo=data['photo'],
                                 chat_id=message.from_user.id,
                                 caption=data['question'],
                                 reply_markup=ikb,
                                 parse_mode='HTML')

    await message.answer(text='Опубликовать?', reply_markup=ikb_public)
    await state.finish()


# @dp.callback_query_handler(lambda x: x.data.startswith('public'))
async def public(callback: CallbackQuery):
    """Публикация/удаление поста"""

    if callback.data.split('_')[-1] == 'not':
        last_message_id = await get_last_message_id()
        await delete_question(last_message_id.last_id + 1)
        await callback.message.delete()
        await callback.message.answer('Пост удален. Создать новый - /create')

    else:

        if data['question'] == '-':
            await bot.send_photo(photo=data['photo'],
                                 chat_id=getenv('CHANEL_ID'),
                                 reply_markup=data['ikb'])
        else:
            await bot.send_photo(photo=data['photo'],
                                 chat_id=getenv('CHANEL_ID'),
                                 caption=f"{data['question']}",
                                 reply_markup=data['ikb'],
                                 parse_mode='HTML')

        await callback.message.delete()
        await update_last_message_id()
        await callback.message.answer('Пост опубликован. Создать новый - /create')


# @dp.callback_query_handler(lambda x: x.data.startswith('vote'))
async def vote(callback: CallbackQuery):
    """Нажатие на инлайн кнопку поста"""
    if callback.message.from_id == int(getenv('BOT_ID')):
        l_id = await get_last_message_id()
        question = await get_question(l_id.last_id + 1)
    else:
        question = await get_question(callback.message.message_id)
    if question.promo:
        user = await bot.get_chat_member(chat_id=getenv('CHANEL_ID'), user_id=callback.from_user.id)
        if user.status == 'left':
            await callback.answer('Подпишитесь, чтобы узнать ответ!', show_alert=True)

    answer = await get_answer(question.id, int(callback.data[-1]))

    if not await get_user_question(callback.from_user.id, question.id):
        await create_user_question(user_id=callback.from_user.id, question_id=question.id)
        await post_counter_increase(answer.id, question.id)

    if question.count == 0:
        question.count += 1
    await callback.answer(
        f"{answer.description}\n\nОтветили так же: {answer.count} чел. ({round(answer.count / question.count * 100)}%)",
        show_alert=True)


async def show_results(callback: CallbackQuery):
    question = await get_question(callback.message.message_id)
    if not await get_user_question(callback.from_user.id, question.id):
        await callback.answer('Сначала нужно ответить')
    else:
        ans = sorted(await get_results(question.id), key=lambda x: x.position)
        text = ''
        for i in range(4):
            text += f'{ans[i].title} - {ans[i].count} ({round(ans[i].count / question.count * 100)}%)\n'

        await callback.answer(f'Статистика📊\n\n{text}\nВсего: {question.count}', show_alert=True)


async def last_post(message: types.Message):
    """Cоздание/обновление last_message_id"""
    last_post_id = await get_last_message_id()
    if not last_post_id:
        await create_last_message_id(last_id=message.forward_from_message_id)
    elif last_post_id.last_id < message.forward_from_message_id:
        await update_last_message_id(id_new=message.forward_from_message_id)

    await message.answer('Спасибо! Создать пост - /create', reply_markup=kb_start)


def create_handlers_register(dp: Dispatcher):
    dp.register_message_handler(last_post, is_forwarded=True, state=check_id,
                                content_types=[types.ContentType.ANY])

    dp.register_callback_query_handler(public, lambda x: x.data.startswith('public'))
    dp.register_callback_query_handler(vote, lambda x: x.data.startswith('vote'))
    dp.register_channel_post_handler(get_any_post, content_types=[types.ContentType.ANY])
    dp.register_callback_query_handler(show_results, text='show_results')
    dp.register_message_handler(keyboard_type, state=PostStateGroup.keyboard_type)
    dp.register_message_handler(add_statistics, state=PostStateGroup.add_statistics)
    dp.register_message_handler(add_statistics_text, state=PostStateGroup.add_statistics_text)
