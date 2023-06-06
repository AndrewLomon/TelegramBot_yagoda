import time
from aiogram import Dispatcher, types
from Keyboards import KeyBoards
from create_bot import bot, db
import MessageBox
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM_admin(StatesGroup):
    admin = State()
    photo = State()
    phDescription = State()

async def manage_admin(message: types.Message):
    await FSM_admin.admin.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text=MessageBox.ADMIN_MESSAGE,
                           reply_markup=KeyBoards.kb_admin)

async def add_admin(message: types.Message):
    try:
        if not db.admin_exists(message.from_user.id):
            db.add_admin(message.from_user.id, message.from_user.username, time.asctime())
            await message.reply(text=f'Теперь вы получаете заказы, {message.from_user.full_name}')
            await message.delete()
        else:
            await message.answer(f'Вы уже в списке администраторов, {message.from_user.full_name}')
    except:
        await message.answer('Не удалось обновить получателя заказов')

async def delete_admin(message: types.Message):
    try:
        if not db.admin_exists(message.from_user.id):
            await message.answer('Вас нет в списке получения заказов')
        else:
            db.delete_admin(message.from_user.id)
            await message.reply(text=f'Теперь вы не будете получать заказы, {message.from_user.full_name}')
            await message.delete()
    except:
        await message.answer('Не удалось удалить админку')

async def get_client_data_admin(message: types.Message):
    if db.admin_exists(message.from_user.id):
        for col in db.get_client_info():
            count = 0
            await bot.send_message(message.from_user.id, '_________________\n')
            await bot.send_message(message.from_user.id, text=f'ID {col[1]}\n'
                                                              f'Время авторизации {col[2]}\n'
                                                              f'Имя {col[3]}\n'
                                                              f'Телефон {col[4]}\n'
                                                              f'Ник @{col[5]}\n'
                                                              f'Адрес: {col[6]}')
            for rowOrder in db.get_client_orders(col[1]):
                count += 1
                await bot.send_message(message.from_user.id, text=f'Заказ №{count}\n'
                                                                  f'Объем клубники: {rowOrder[0]}\n'
                                                                  f'Дата заказа: {rowOrder[1]}')
    else:
        await message.answer('Вы не в списке администраторов')



async def manage_admin_close(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome back',
                           reply_markup=KeyBoards.kb_main)
    await state.finish()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(manage_admin, is_owner=True, commands=['admin'], commands_prefix="!/")
    dp.register_message_handler(add_admin, lambda message: message.text.startswith('Добавить'), state=FSM_admin.admin)
    dp.register_message_handler(delete_admin, lambda message: message.text.startswith('Удалить'), state=FSM_admin.admin)
    dp.register_message_handler(get_client_data_admin, lambda message: message.text.startswith('Выгрузить'), state=FSM_admin.admin)
    dp.register_message_handler(manage_admin_close, lambda message: message.text.startswith('Закрыть'), state='*')
