import logging
import time
import string

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import MessageBox
from Keyboards import KeyBoards, InlineKB
from create_bot import bot


class FSM_client(StatesGroup):
    start_order = State()
    type_product = State()
    sub_type_product = State()
    volume_product = State()
    extra_volume_product = State()
    client_location = State()
    client_phone = State()

# @dp.message_handler(commands=['start','help','info','Discounts','Make_order'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await bot.send_message(chat_id=message.from_user.id,
                           text=MessageBox.START_MESSAGE,
                           reply_markup=KeyBoards.kb_main)
    await message.delete()


async def command_help(message: types.Message):
    await message.reply(text=MessageBox.HELP_MESSAGE)
    await message.delete()


async def command_info(message: types.Message):
    await message.reply(text=MessageBox.INFO_MESSAGE)
    await message.delete()


async def command_discount(message: types.Message):
    await message.reply(text=MessageBox.DISCOUNT_MESSAGE)  # TODO Make a subsrption on discount updates
    await message.delete()


# Начало диалога заказа продукта
async def command_makeorder(message: types.Message):
    uid = message.from_user.id
    uname = message.from_user.full_name
    try:
        await FSM_client.start_order.set()
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
    await message.answer('Оформление заказа остановлено. \n'
                         'Чтобы начать процесс заново нажмите \n/Make_order')
    await state.finish()

async def request_extra_volume(message: types.Message, state: FSMContext):
    #TODO: Сделать проверку, в случае рассады на кратность 64, а в случае клубники больше 9
    await state.update_data(extra_volume_product=message.text)
    print(await state.get_data())
    await message.answer(text=MessageBox.MORE_ANSWER)
    await FSM_client.client_location.set()

async def request_location(message: types.Message, state: FSMContext): #TODO: Сделать проверку, изменив пример локации
    await state.update_data(client_location=message.text)
    print(await state.get_data())
    await message.answer('Введите пожалуйста ваш номер телефона')
    await FSM_client.client_phone.set()
async def request_phone(message: types.Message, state: FSMContext): #TODO: Сделать проверку на телефон +7
    await state.update_data(client_phone=message.text)
    result = await state.get_data()
    await message.answer('Превосходно! Заказ сформирован.\n'
                         'Если у вас остались вопросы то вы можете всегда связаться с нами через команду\n'
                         '/Contacts')
    await bot.send_message(326374284, result) #TODO: Добавить handler with hidden command for recieving admin's ID
    await state.finish()
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_info, commands=['info'])
    dp.register_message_handler(command_discount, commands=['Discounts'])
    # TODO: Добавить функцию с инлайн клавиатурой и сылками на нужные контакты
    dp.register_message_handler(command_makeorder, commands=['Make_order'], state=None)
    dp.register_message_handler(cancel_handler, commands=['Cancel'], state='*')
    dp.register_message_handler(request_extra_volume, state=FSM_client.extra_volume_product)
    dp.register_message_handler(request_location, state=FSM_client.client_location)
    dp.register_message_handler(request_phone, state=FSM_client.client_phone)

