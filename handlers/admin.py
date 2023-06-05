from aiogram import Dispatcher, types
from Config import RECEIVE_ID
from Keyboards import KeyBoards
from create_bot import bot
import MessageBox
from aiogram.dispatcher import FSMContext
from handlers.client import FSM_client
from db import BotDB


BotDB = BotDB('yagoda.db')

async def manage_admin(message: types.Message):
    await FSM_client.admin.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text=MessageBox.ADMIN_MESSAGE,
                           reply_markup=KeyBoards.kb_admin)

async def add_admin(message: types.Message):
    try:
        if message.from_user.id not in RECEIVE_ID:
            RECEIVE_ID.append(message.from_user.id)
            await message.reply(text=f'Теперь вы получаете заказы, {message.from_user.full_name}')
            await message.delete()
            return RECEIVE_ID
        else:
            await message.answer(f'Вы уже в списке администраторов, {message.from_user.full_name}')
    except:
        await message.answer('Не удалось обновить получателя заказов')

async def delete_admin(message: types.Message):
    try:
        if message.from_user.id in RECEIVE_ID:
            RECEIVE_ID.remove(message.from_user.id)
            await message.reply(text=f'Теперь вы не будете получать заказы, {message.from_user.full_name}')
            await message.delete()
            return RECEIVE_ID
    except:
        await message.answer('Не удалось удалить админку')

async def get_client_data_admin(message: types.Message):
    for row in BotDB.get_client_info():
        count = 0
        await bot.send_message(message.from_user.id, text=f'ID {row[1]}\n'
                                            f'Время авторизации {row[2]}\n'
                                            f'Имя {row[3]}\n'
                                            f'Телефон {row[4]}\n'
                                            f'Ник @{row[5]}\n'
                                            f'Адрес: {row[6]}')
        for rowOrder in BotDB.get_client_orders(row[1]):
            count += 1
            await bot.send_message(message.from_user.id, text=f'Заказ №{count}\n'
                                                 f'Объем клубники: {rowOrder[0]}\n'
                                                 f'Дата заказа: {rowOrder[1]}')

async def manage_admin_close(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome back',
                           reply_markup=KeyBoards.kb_main)
    await state.finish()
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(manage_admin, commands=['admin'], commands_prefix="!/")
    dp.register_message_handler(add_admin, lambda message: message.text.startswith('Добавить'), state=FSM_client.admin)
    dp.register_message_handler(delete_admin, lambda message: message.text.startswith('Удалить'), state=FSM_client.admin)
    dp.register_message_handler(get_client_data_admin, lambda message: message.text.startswith('Выгрузить'), state=FSM_client.admin)
    dp.register_message_handler(manage_admin_close, lambda message: message.text.startswith('Закрыть'), state=FSM_client.admin)