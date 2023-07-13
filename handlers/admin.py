import time
from aiogram import Dispatcher, types

import Config
from Keyboards import KeyBoards
from create_bot import bot, db
import MessageBox
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class FSM_admin(StatesGroup):
    admin = State()
    dbase = State()
    photo = State()
    phName = State()
    phDescription = State()


"""Функции главного окна админки"""


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
        await bot.send_message(Config.BOT_OWNERS[0], "Провалилась попытка добавить админа")


async def delete_admin(message: types.Message):
    try:
        if not db.admin_exists(message.from_user.id):
            await message.answer("Вас нет в списке получения заказов")
        else:
            if len(db.get_admin_id()) <= 1:
                await message.answer('На данный моменты вы единственный админ, удалить вас из рассылки не получится')
            else:
                db.delete_admin(message.from_user.id)
                await message.reply(text=f'Теперь вы не будете получать заказы, {message.from_user.full_name}')
                await message.delete()
    except:
        await message.answer('Не удалось удалить админку')
        await bot.send_message(Config.BOT_OWNERS[0], "Провалилась попытка удалить админа")


async def dbase_menu_open(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Что будем делать с БД?',
                           reply_markup=KeyBoards.kb_db)
    await FSM_admin.dbase.set()


async def manage_admin_close(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome back',
                           reply_markup=KeyBoards.kb_main)
    await state.finish()


# Дальше команды для управления БД
"""Загрузка опций в меню"""


async def cmd_updateMenu(message: types.Message):
    await FSM_admin.photo.set()
    await message.reply('Чтобы добавить позицию нужно выполнить 3 шага:\n'
                        '1. Отправить фото\n'
                        '2. Написать название фото (необходимо для БД)\n'
                        '3. Написать сопровождающее собщение которое быдет видно покупателям\n'
                        '<b>Скидывай сюда нужную тебе фотографию</b>', parse_mode='html')


async def upload_photo(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSM_admin.next()
        await message.reply('1. Отправить фото✅\n'
                            '2. <b>Напиши название фото (необходимо для БД)</b>\n', parse_mode='html')
    except:
        await message.answer('Загрузите как фото, а не как файл')
        await bot.send_message(Config.BOT_OWNERS[0], "Провалилась попытка загрузки фото")


async def upload_phName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phName'] = message.text
    await FSM_admin.next()
    await message.reply('1. Отправить фото✅\n'
                        '2. Написать название фото (необходимо для БД)✅\n'
                        '3. <b>Напиши сопровождающее собщение которое будет видно покупателям</b>', parse_mode='html')


async def upload_phDescription(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phDescription'] = message.text
    result = await state.get_data()
    db.add_menu(result['photo'], result['phName'], result['phDescription'])
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Всё готово✅',
                           reply_markup=KeyBoards.kb_db)
    await FSM_admin.dbase.set()


"""Удаление опций из меню"""


async def cmd_delete_menu(message: types.Message):
    menu = db.get_menu()
    if bool(len(menu)):
        for col in menu:
            await bot.send_photo(message.from_user.id, col[1], f'\n{col[3]}')
            await bot.send_message(message.from_user.id,
                                   text='☝️',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить', callback_data=f'del {col[2]}')))
    else:
        await message.answer('На данный момент нет подгруженого меню')
    await message.delete()


async def run_delete_menu(callback: types.CallbackQuery):
    cb = callback.data.replace('del ', '')
    db.delete_menu(cb)
    await callback.answer(f'{cb} успешно удалено', show_alert=True)


"""Выгрузка клиентов с заказами и выход из БД"""


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



async def get_admins_list(message: types.Message):
    try:
        for admin in db.get_admin_list():
            await bot.send_message(message.from_user.id, text=f'ID: {admin[1]}\n'
                                                              f'Name: {admin[2]}')
    except:
        await message.answer('Не удалось получить список получателей рассылки заказов')
        await bot.send_message(Config.BOT_OWNERS[0], "Провалилась попытка получить список тех кто получает заказы")



async def dbase_menu_close(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(chat_id=message.from_user.id,
                           text='С возвращением в админку',
                           reply_markup=KeyBoards.kb_admin)
    await FSM_admin.admin.set()


def register_handlers_admin(dp: Dispatcher):
    # Функции главного окна админки
    dp.register_message_handler(manage_admin, is_owner=True, commands=['admin'], commands_prefix="!/")
    dp.register_message_handler(manage_admin_close, lambda message: message.text.startswith('Закрыть'), state='*')
    dp.register_message_handler(add_admin, lambda message: message.text.startswith('Добавить'), state=FSM_admin.admin)
    dp.register_message_handler(delete_admin, lambda message: message.text.startswith('Удалить'), state=FSM_admin.admin)
    dp.register_message_handler(dbase_menu_open, lambda message: message.text.startswith('БД'),
                                state=FSM_admin.admin)

    # Загрузка в меню
    dp.register_message_handler(cmd_updateMenu, lambda message: message.text.startswith('Обновить'),
                                state=FSM_admin.dbase)
    dp.register_message_handler(upload_photo, content_types=['photo'], state=FSM_admin.photo)
    dp.register_message_handler(upload_phName, state=FSM_admin.phName)
    dp.register_message_handler(upload_phDescription, state=FSM_admin.phDescription)

    # Удаление опций из меню
    dp.register_message_handler(cmd_delete_menu, lambda message: message.text.startswith('Удалить опции'),
                                state=FSM_admin.dbase)
    dp.register_callback_query_handler(run_delete_menu, lambda x: x.data and x.data.startswith('del '),
                                       state=FSM_admin.dbase)

    # Выгрузка клиентов с заказами и выход из БД
    dp.register_message_handler(get_admins_list, lambda message: message.text.startswith('Лист'),
                                state=FSM_admin.dbase)
    dp.register_message_handler(get_client_data_admin, lambda message: message.text.startswith('Выгрузить'),
                                state=FSM_admin.dbase)
    dp.register_message_handler(dbase_menu_close, lambda message: message.text.startswith('Вернуться'),
                                state=FSM_admin.dbase)
