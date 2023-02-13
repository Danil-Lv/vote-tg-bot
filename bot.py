from aiogram import executor, types, Dispatcher

from create_bot import dp, bot
from handlers.commands import commands_handlers_register
from db.database import create_db
from handlers.handling_post import create_handlers_register
from handlers.create_post import reg_handlers_register

# id юзеров, которым разрешен доступ
users = (717218923, 812456591)

commands_handlers_register(dp)
create_handlers_register(dp)
reg_handlers_register(dp)


async def on_startup(_):
    print('Бот запущен')
    await create_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

# @dp.message_handler(is_forwarded=True, content_types=['photo'])
# async def some(message: types.Message):
#     message_chanel_id = message.forward_from_message_id
#     await message.answer('hello')

# -1001612936953

# @dp.message_handler(chat_type=[types.ChatType.GROUP])
# async def get_message(message: types.Message):
#     if message.chat.id == "id первой группы":
#         await bot.send_message(
#             "id второй группы",
#             text= f"User {message.from_user.username}:\n" + message.text
#         )
