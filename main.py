# This is a new Telegram Bot  - Education version
import time
import logging
from aiogram import Bot, Dispatcher, executor, types

import KeyBoards
from KeyBoards import kb_main, ikb_order, ikb_Straw, ikb_type_seed
from Config import TOKEN
import MessageBox


#Just warning that bot is working
print('Okay, lets go!')

# These are constant variables
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# Here are all functions that bot is using
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await bot.send_message(chat_id=message.from_user.id,
                           text=MessageBox.START_MESSAGE)

@dp.message_handler(commands=['help'])
async def command_help(message:types.Message):
    await message.reply(text=MessageBox.HELP_MESSAGE)
    await message.delete()

@dp.message_handler(commands=['info'])
async def command_info(message:types.Message):
    await message.reply(text=MessageBox.INFO_MESSAGE)
    await message.delete()
@dp.message_handler(commands=['Discounts'])
async def command_info(message:types.Message):
    await message.reply(text=MessageBox.DISCOUNT_MESSAGE) # TODO Make a subsrption on discount updates
    await message.delete()

@dp.message_handler(commands=['Make_order'])
async def command_make_order(message:types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Что бы вы хотели заказать?',
                           reply_markup=ikb_order)
    await message.delete()

@dp.callback_query_handler()
async def callback_make_order(callback: types.CallbackQuery):
    if callback.data == 'Product1':
        await callback.message.reply(text='Какой вы хотите объем?',
                                     reply_markup=KeyBoards.ikb_Straw)
    await callback.message.reply(text='Какой сорт вас интересует?',
                                 reply_markup=ikb_type_seed)



if __name__ == '__main__':
    executor.start_polling(dp)
