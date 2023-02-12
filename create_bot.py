from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv



load_dotenv()

bot = Bot(getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
