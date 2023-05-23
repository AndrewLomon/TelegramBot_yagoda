import logging
import time
import string
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import MessageBox
from Keyboards import KeyBoards, InlineKB
from create_bot import bot
from db import BotDB
from Config import RECEIVE_ID

ID = None # ID нужно поменять через команду admin_id

class FSM_client(StatesGroup):
    type_product = State()
    sub_type_product = State()
    volume_product = State()
    volume_product2 = State()
    extra_volume_product = State()
    client_location = State()
    client_phone = State()

#Подключение БД.
BotDB = BotDB('yagoda.db')

async def command_start(message: types.Message):
    userID = message.from_user.id
    name = message.from_user.full_name
    nick_name = message.from_user.username
    if not BotDB.user_exists(userID):
        BotDB.add_client(userID, time.asctime(), name, nick_name)
    await bot.send_message(chat_id=message.from_user.id,
                           text=MessageBox.START_MESSAGE,
                           reply_markup=KeyBoards.kb_main)
    await message.delete()

async def command_admin_id(message: types.Message):
    RECEIVE_ID = message.from_user.id
    await message.reply(text=f'Теперь вы получаете заказы, {message.from_user.full_name}')
    await message.delete()
    return RECEIVE_ID

async def command_help(message: types.Message):
    await message.reply(text=MessageBox.HELP_MESSAGE)
    await message.delete()


async def command_info(message: types.Message):
    await message.reply(text=MessageBox.INFO_MESSAGE,
                        parse_mode='html')
    await message.delete()


async def command_discount(message: types.Message):
    await message.reply(text=MessageBox.DISCOUNT_MESSAGE)
    await message.delete()


# Начало диалога заказа продукта
async def command_makeorder(message: types.Message):
    uid = message.from_user.id
    uname = message.from_user.full_name
    try:
        await FSM_client.type_product.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Что бы вы хотели заказать, {uname}?',
                               reply_markup=InlineKB.ikb_order)
        await message.delete()
    except Exception:
        await bot.send_message(uid, 'Что-то пошло не так с командой сделать заказ')


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer('Оформление заказа остановлено')
    await state.finish()

async def request_extra_volume(message: types.Message, state: FSMContext):
    result = await state.get_data()
    if 'volume_product2' in result:
        if int(message.text) % 64 == 0 and int(message.text) > 512:
            await state.update_data(extra_volume_product=message.text)
            await message.answer(text=MessageBox.MORE_ANSWER,
                                 parse_mode='html')
            await FSM_client.client_location.set()
        else:
            await message.answer('Извините, количество кустов рассады должно быть кратно 64 и больше 512')
    else:
        if int(message.text) > 9:
            await state.update_data(extra_volume_product=message.text)
            await message.answer(text=MessageBox.MORE_ANSWER,
                                 parse_mode='html')
            await FSM_client.client_location.set()
        else:
            await message.answer('Извините, объем клубники должен быть больше 9кг')

async def request_location(message: types.Message, state: FSMContext):
    if 'ул' in message.text or 'д.' in message.text or 'кв.' in message.text:
        await state.update_data(client_location=message.text)
        await message.answer('Введите пожалуйста ваш номер телефона\n'
                             '<b>Пример:</b> 7987*******',
                             parse_mode='html')
        await FSM_client.client_phone.set()
    else:
        await message.answer('Не могу разобрать адрес, проверьте сходится ли он с примером и попробуйте ещё раз')

async def request_phone(message: types.Message, state: FSMContext):
    if message.text.startswith('7') and len(message.text) == 11:
        user_name = message.from_user.username
        user_full_name = message.from_user.full_name
        await state.update_data(client_phone=message.text)
        result = await state.get_data()
        await message.answer(text=MessageBox.Respond_request_phone)
        await bot.send_message(RECEIVE_ID, f'<b>Новый заказ</b>:\n'
                                   f'<b>Время</b>: {time.asctime()}\n'
                                   f'<b>ФИО</b>: {user_full_name}\n'
                                   f'@{user_name}\n'
                                   f'<b>ЗАКАЗ</b>:\n{result}',
                               parse_mode='html')
        # BotDB.record_client_data(result['client_phone'], result['client_location'])
        # BotDB.record_order(message.from_user.id,result['start_order'], result['sub_type_product'], result['volume_product'])

        await state.finish()
    else:
        await message.answer('Не могу разобрать ваш номер телефона, сверьтесь с примером и попробуйте ещё раз')

async def unknown_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id == message.from_user.id:
        await message.answer('Я вас не понимаю, попробуйте ещё раз или выберете одну из команд ниже')
    else:
        await message.answer('Ничего страшного мы скоро с вами свяжемся')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_admin_id, commands=['admin_id'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_info, commands=['info'])
    dp.register_message_handler(command_discount, lambda message: message.text.startswith('Скидки'))
    # TODO: Добавить функцию с инлайн клавиатурой и сылками на нужные контакты
    dp.register_message_handler(command_makeorder, lambda message: message.text.startswith('Заказать'), state=None)
    dp.register_message_handler(cancel_handler, lambda message: message.text.startswith('Отмена'), state='*')
    dp.register_message_handler(request_extra_volume, state=FSM_client.extra_volume_product)
    dp.register_message_handler(request_location, state=FSM_client.client_location)
    dp.register_message_handler(request_phone, state=FSM_client.client_phone)
    dp.register_message_handler(unknown_handler)

