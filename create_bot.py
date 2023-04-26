from aiogram import Bot
from aiogram import Dispatcher
from Config import TOKEN
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

my_storage = MemoryStorage()


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=my_storage)
