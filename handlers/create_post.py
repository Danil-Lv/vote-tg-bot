from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import kb_create_post, kb_question, kb_type

check_id = State()
class PostStateGroup(StatesGroup):
    # last_post = State()
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
    promo = State()
    keyboard_type = State()
    add_statistics = State()
    add_statistics_text = State()


# @dp.message_handler(state='*', text='Стоп')

async def cancel_handler(message: types.Message, state: FSMContext):
    """Отмена создания поста"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отменено создание поста', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(state=PostStateGroup.question)
async def question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text

    await message.answer('Напиши вариант ответа 1.', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b1)
async def ans1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans1'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b1_desc)
async def ans1_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans1_desc'] = message.text

    await message.answer('Напиши 2 вариант ответа.', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b2)
async def ans2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans2'] = message.text

    await message.answer('Напиши описание ответа.', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b2_desc)
async def ans2_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans2_desc'] = message.text

    await message.answer('Напиши 3 вариант ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b3)
async def ans3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans3'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b3_desc)
async def ans3_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans3_desc'] = message.text

    await message.answer('Напиши 4 вариант ответа', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b4)
async def ans4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans4'] = message.text

    await message.answer('Напиши описание ответа', reply_markup=kb_create_post)
    await PostStateGroup.next()


# @dp.message_handler(state=PostStateGroup.b4_desc)
async def ans4_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ans4_desc'] = message.text

    await message.answer('Теперь пришли фотографию', reply_markup=kb_create_post)

    await PostStateGroup.next()


# @dp.message_handler(content_types=['photo'], state=PostStateGroup.photo)
async def photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.answer('Это рекламный пост?', reply_markup=kb_question)
    await PostStateGroup.next()


async def promo(message: types.Message, state):
    async with state.proxy() as data:
        if message.text == 'Да':
            data['promo'] = True
        elif message.text == 'Нет':
            data['promo'] = False

    await message.answer('Вид клавиатуры', reply_markup=kb_type)
    await PostStateGroup.next()




def reg_handlers_register(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', text='Отмена')
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
    dp.register_message_handler(promo, state=PostStateGroup.promo)
    # dp.register_message_handler(keyboard_type, state=PostStateGroup.keyboard_type)

