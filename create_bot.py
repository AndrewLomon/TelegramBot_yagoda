from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import Config
from db import BotDB
from filters import IsOwnerFilter, IsAdminFilter

my_storage = MemoryStorage()
db = BotDB('yagoda.db')

bot = Bot(token=Config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=my_storage)

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)

