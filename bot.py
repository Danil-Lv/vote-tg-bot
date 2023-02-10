from aiogram import executor
from create_bot import dp
from handlers.commands import commands_handlers_register

from db.database import create_db

from handlers.create_post import create_handlers_register

commands_handlers_register(dp)
create_handlers_register(dp)


async def on_startup(_):
    print('Yes')
    await create_db()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
