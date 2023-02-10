from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b_yes = KeyboardButton(text='Да')
b_no = KeyboardButton(text='Нет')

kb.add(b_yes, b_no)


kb_not_correct = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

b_defaul = """
Неверно❌

Попробуй еще👍
"""

kb_not_correct.add(b_defaul)

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
create_btn = KeyboardButton(text='/create')
kb_start.add(create_btn)

kb_create_post = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
stop_btn = KeyboardButton(text='Прекратить создание поста')
kb_create_post.add(b_defaul, stop_btn)

ikb_public = InlineKeyboardMarkup()
ikb_public_yes = InlineKeyboardButton(text='Да', callback_data='public')
ikb_public_no = InlineKeyboardButton(text='Нет', callback_data='public_not')
ikb_public.add(ikb_public_yes, ikb_public_no)