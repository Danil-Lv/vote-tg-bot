
import logging

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook

from create_bot import dp, bot
from handlers.commands import commands_handlers_register
from db.database import create_db
from handlers.handling_post import create_handlers_register
from handlers.create_post import reg_handlers_register

# id юзеров, которым разрешен доступ
users = (717218923, 812456591)


WEBHOOK_HOST = 'https://3e23-212-113-123-72.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 5000

commands_handlers_register(dp)
create_handlers_register(dp)
reg_handlers_register(dp)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(_):
    print('Бот запущен')
    await create_db()
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Работа бота завершена')

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


