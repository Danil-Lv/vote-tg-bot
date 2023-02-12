from os import getenv

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


from create_bot import bot
from keyboards import kb_create_post, ikb_public
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

    await show_post(message, state)


# @dp.message_handler()
async def show_post(message: types.Message, state):
    """Вывод сообщения при модерации"""
    global data
    async with state.proxy() as data:
        if data['kb_type'] == 'big':
            rows = 1
        elif data['kb_type'] == 'small':
            rows = 2
        ikb = InlineKeyboardMarkup(row_width=rows)
        ans1_btn = InlineKeyboardButton(text=f'{data["ans1"]}', callback_data='vote1')
        ans2_btn = InlineKeyboardButton(text=f'{data["ans2"]}', callback_data='vote2')
        ans3_btn = InlineKeyboardButton(text=f'{data["ans3"]}', callback_data='vote3')
        ans4_btn = InlineKeyboardButton(text=f'{data["ans4"]}', callback_data='vote4')

        show_results_btn = InlineKeyboardButton(text='Статистика ответов📊', callback_data='show_results')

        ikb.add(ans1_btn, ans2_btn, ans3_btn, ans4_btn).insert(show_results_btn)
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
async def public(callback: CallbackQuery, state: FSMContext):
    """Вопрос о публикации поста"""
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
        await callback.message.answer('Пост опубликован')


# @dp.callback_query_handler(lambda x: x.data.startswith('vote'))
async def vote(callback: CallbackQuery):
    """Нажатие на инлайн кнопку поста"""
    if callback.message.from_id == int(getenv('TOKEN').split(':')[0]):
        l_id = await get_last_message_id()
        question = await get_question(l_id.last_id+1)
    else:
        question = await get_question(callback.message.message_id)
    if question.promo:
        user = await bot.get_chat_member(chat_id=getenv('CHANEL_ID'), user_id=callback.from_user.id)
        if user.status == 'left':
            await callback.answer('Подпишитесь на канал, чтобы узнать ответ', show_alert=True)

    answer = await get_answer(question.id, int(callback.data[-1]))

    if not await get_user_question(callback.from_user.id, question.id):
        await create_user_question(user_id=callback.from_user.id, question_id=question.id)
        await post_counter_increase(answer.id, question.id)

    if question.count == 0:
        question.count += 1
    await callback.answer(
        f"{answer.description}\n\nОтветили так же: {answer.count} чел. ({round(answer.count / question.count * 100)}%)",
        show_alert=True)

async def vote_check(callback: CallbackQuery):
    question = await get_question(callback.message.message_id)
    answer = await get_answer(question.id, int(callback.data[-1]))

    await callback.answer(show_alert=True)

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

    await message.answer('Напиши вопрос', reply_markup=kb_create_post)
    await message.answer(text='Если хочешь создать пост без вопроса напиши -')
    await PostStateGroup.next()




def create_handlers_register(dp: Dispatcher):
    dp.register_message_handler(last_post, is_forwarded=True, state=PostStateGroup.last_post,
                                content_types=[types.ContentType.ANY])

    dp.register_callback_query_handler(public, lambda x: x.data.startswith('public'))
    dp.register_callback_query_handler(vote, lambda x: x.data.startswith('vote'))
    dp.register_channel_post_handler(get_any_post, content_types=[types.ContentType.ANY])
    dp.register_message_handler(keyboard_type, state=PostStateGroup.keyboard_type)
    dp.register_callback_query_handler(show_results, text='show_results')
