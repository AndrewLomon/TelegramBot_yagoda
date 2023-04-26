# This is a new Telegram Bot  - Education version
from aiogram import Bot, Dispatcher, executor, types
import callback
from create_bot import dp
from handlers import client, others

async def on_startup(_):
    print('Okay, lets go!')



client.register_handlers_client(dp)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
