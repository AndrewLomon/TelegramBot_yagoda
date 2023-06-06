import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile

import MessageBox
from Keyboards import KeyBoards, InlineKB
from create_bot import bot, db


class FSM_client(StatesGroup):
    volume_berry = State()
    client_location = State()
    client_phone = State()


async def command_start(message: types.Message):
    userID = message.from_user.id
    name = message.from_user.full_name
    nick_name = message.from_user.username
    if not db.user_exists(userID):
        db.add_client(userID, time.asctime(), name, nick_name)
    await bot.send_message(chat_id=message.from_user.id,
                           text=MessageBox.START_MESSAGE,
                           reply_markup=KeyBoards.kb_main)
    await message.delete()

async def command_help(message: types.Message):
    await message.reply(text=MessageBox.HELP_MESSAGE)
    await message.delete()


async def command_info(message: types.Message):
    await message.reply(text=MessageBox.INFO_MESSAGE,
                        parse_mode='html')
    await message.delete()


async def command_discount(message: types.Message):
    await message.reply(text=MessageBox.DISCOUNT_MESSAGE, parse_mode='html')
    await message.delete()

async def get_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    photo_url3 = InputFile('photos/Strawberry.jpg')
    await bot.send_photo(message.from_user.id, photo=photo_url3)
    await message.answer('Выше представлено наше меню.\n'
                         'Чтобы начать оформление заказа нажмите на кнопку в меню\n'
                         '<b>Сделать заказ</b> 🍓',parse_mode='html')
    await message.delete()

# Начало диалога заказа продукта
async def command_makeorder(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    uname = message.from_user.full_name
    try:
        current_state = await state.get_state()
        if current_state:
            await state.finish()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Вы можете заказать клубнику, следуя инструкции 😀 \n'
                                    f'Выберете необходимый объем, {uname}?',
                               reply_markup=InlineKB.ikb_Straw)
        await FSM_client.volume_berry.set()
        await message.delete()
    except:
        await bot.send_message(uid, 'Что-то пошло не так с командой сделать заказ')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text='Процесс оформления заказа не начат. Чтобы начать оформление заказа нажмите на кнопку в меню\n'
                             '<b>Сделать заказ</b> 🍓',
                             parse_mode='html')
        return
    await message.answer('Оформление заказа остановлено')
    await state.finish()

async def request_extra_volume_berry(message: types.Message, state: FSMContext):
    try:
        if int(message.text) > 9 or int(message.text) == 3 or int(message.text) == 6:
            await state.update_data(volume_berry=message.text)
            await message.answer(text=MessageBox.MORE_ANSWER,
                                 parse_mode='html')
            await FSM_client.client_location.set()
            await message.delete()
        else:
            await message.answer('Извините, объем клубники должен быть больше равен 3, 6, 9кг или больше')
    except:
        await message.answer('Выберите пожалуйста опцию выше или впишите число')


async def request_location(message: types.Message, state: FSMContext):
    try:
        if 'ул' in message.text or 'д.' in message.text or 'кв.' in message.text:
            await state.update_data(client_location=message.text)
            await message.answer('Введите пожалуйста ваш номер телефона\n'
                                 '<b>Пример:</b> 7987*******',
                                 parse_mode='html')
            await FSM_client.client_phone.set()
            await message.delete()
        else:
            await message.answer('Не могу разобрать адрес, проверьте сходится ли он с примером и попробуйте ещё раз')
    except:
        await message.answer('Я вас не понимаю, попробуйте ещё раз или выберете одну из команд ниже')

async def request_phone(message: types.Message, state: FSMContext):
    try:
        if message.text.startswith('7') and len(message.text) == 11:
            user_name = message.from_user.username
            user_full_name = message.from_user.full_name
            await state.update_data(client_phone=message.text)
            result = await state.get_data()
            await message.answer(text=MessageBox.Respond_request_phone)
            await message.delete()
            admins = db.get_admin_id()
            # Рассылка для админов заказов
            for admin_n in admins:
                await bot.send_message(admin_n[0], f'<b>Новый заказ</b>:\n'
                                                   f'<b>Время</b>: {time.asctime()}\n'
                                                   f'<b>ФИО</b>: {user_full_name}\n'
                                                   f'@{user_name}\n'
                                                   f'<b>ЗАКАЗ</b>:\n{result}',
                                       parse_mode='html')
            # Запись данных в БД
            db.record_client_data(result['client_phone'], result['client_location'], message.from_user.id)
            db.record_order(message.from_user.id, result['volume_berry'], time.asctime())
            await state.finish()
        else:
            await message.answer('Не могу разобрать ваш номер телефона, сверьтесь с примером и попробуйте ещё раз')
    except:
        await message.answer('Я вас не понимаю, попробуйте ещё раз или выберете одну из команд ниже')


def register_handlers_client(dp: Dispatcher):
    #Объявление функций обработки команд
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_info, commands=['info'])
    dp.register_message_handler(command_discount, lambda message: message.text.startswith('Скидки'))
    # TODO: Добавить функцию с инлайн клавиатурой и сылками на нужные контакты
    dp.register_message_handler(command_makeorder, lambda message: message.text.startswith('Сделать'), state='*')

    #Объявление функций обработки команд с машиной состояний
    dp.register_message_handler(cancel_handler, lambda message: message.text.startswith('Отмена'), state='*')
    dp.register_message_handler(get_menu, lambda message: message.text.startswith('Меню'), state='*')
    dp.register_message_handler(request_extra_volume_berry, state=FSM_client.volume_berry)
    dp.register_message_handler(request_location, state=FSM_client.client_location)
    dp.register_message_handler(request_phone, state=FSM_client.client_phone)
    # dp.register_message_handler(unknown_handler)

