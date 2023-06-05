# This is Telegram Bot for Srawberry shop
from aiogram import executor
import callback
from create_bot import dp
from handlers import client, admin


async def on_startup(_):
    print('Okay, lets go!')



#Выполнение зарегистрированных функций
admin.register_handlers_admin(dp)
callback.register_handlers_callback(dp)
client.register_handlers_client(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
