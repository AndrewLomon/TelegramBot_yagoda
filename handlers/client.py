import time
import logging

from aiogram import types, Dispatcher

from create_bot import bot, dp
import MessageBox
from Keyboards import KeyBoards, InlineKB


# @dp.message_handler(commands=['start','help','info','Discounts','Make_order'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
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
async def command_makeorder(message: types.Message):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Что бы вы хотели заказать?',
                               reply_markup=InlineKB.ikb_order)
        await message.delete()
def register_handlers_client(dp : Dispatcher):
        dp.register_message_handler(command_start, commands=['start'])
        dp.register_message_handler(command_help, commands=['help'])
        dp.register_message_handler(command_info, commands=['info'])
        dp.register_message_handler(command_discount, commands=['Discounts'])
        dp.register_message_handler(command_makeorder, commands=['Make_order'])