from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""Создание поста"""
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
create_btn = KeyboardButton(text='/create')
kb_start.add(create_btn)

"""Отмена содания поста/шаблон невернного ответа"""
kb_create_post = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
stop_btn = KeyboardButton(text='Отмена')
b_default = "Неверно❌\n\nПопробуй еще👍"
kb_create_post.add(b_default, stop_btn)

"""Подтверждение публикации"""
ikb_public = InlineKeyboardMarkup()
ikb_public_yes = InlineKeyboardButton(text='Да', callback_data='public')
ikb_public_no = InlineKeyboardButton(text='Нет', callback_data='public_not')
ikb_public.add(ikb_public_yes, ikb_public_no)

"""Выбор типа поста, рекламный/обычный"""
kb_question = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_question_yes = KeyboardButton(text='Да')
kb_question_no = KeyboardButton(text='Нет')
kb_question.add(kb_question_yes, kb_question_no)


"""Выбор клавиатуры"""
kb_type = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_type_big = KeyboardButton(text='Большая')
kb_type_small = KeyboardButton(text='Компактная')
kb_type_one_row = KeyboardButton(text='В строку')
kb_type.add(kb_type_big, kb_type_small).add(kb_type_one_row)

"""Значение по умолчанию для кнопки статистики"""
kb_statistic = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_statistic_text = KeyboardButton(text='Статистика ответов📊')
kb_statistic.add(kb_statistic_text)

