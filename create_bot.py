from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()
my_storage = MemoryStorage()


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=my_storage)
