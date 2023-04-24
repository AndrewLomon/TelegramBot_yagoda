# This is a new Telegram Bot  - Education version
import time
import logging
from aiogram import Bot, Dispatcher, executor, types
import string
import KeyBoards
from KeyBoards import kb_main, ikb_order, ikb_Straw, ikb_type_seed
from Config import TOKEN
import MessageBox


#Just a warning that bot is working
print('Okay, lets go!')

# These are constant variables
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

class Consumer:
    def fio(self,fio:string):
        self.fio = fio
    def product(self,product):
        self.product = product

Purchaser = Consumer()
Purchaser.fio()

# Here are all functions that bot is using
@dp.message_handler(commands=['start','help','info','Discounts','Make_order'])
async def command_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    if message.text == '/start':
        await bot.send_message(chat_id=message.from_user.id,
                               text=MessageBox.START_MESSAGE,
                               reply_markup=kb_main)
    elif message.text == '/help':
        await message.reply(text=MessageBox.HELP_MESSAGE)
        await message.delete()
    elif message.text == '/info':
        await message.reply(text=MessageBox.INFO_MESSAGE)
        await message.delete()
    elif message.text == '/Discounts':
        await message.reply(text=MessageBox.DISCOUNT_MESSAGE)  # TODO Make a subsrption on discount updates
        await message.delete()
    elif message.text == '/Make_order':
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Что бы вы хотели заказать, {user_full_name}?',
                               reply_markup=ikb_order)
        await message.delete()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберите одну из функций в списке /help')
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Product'))
async def callback_make_order(callback: types.CallbackQuery):
    if callback.data == 'Product1':
        await callback.message.reply(text='Сколько килограм вы хотите заказать?',
                                     reply_markup=KeyBoards.ikb_Straw)
    elif callback.data == 'Product2':
        await callback.message.reply(text='Какой сорт вас интересует?',
                                     reply_markup=KeyBoards.ikb_type_seed)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('value'))
async def callback_kg_value(callback: types.CallbackQuery):
    if callback.data == 'value3':
        await callback.message.reply(text=MessageBox.KG3_ANSWER)
    elif callback.data == 'value6':
        await callback.message.reply(text=MessageBox.KG6_ANSWER)
    elif callback.data == 'value9':
        await callback.message.reply(text=MessageBox.KG9_ANSWER)
    elif callback.data == 'value_more':
        await callback.message.reply(text=MessageBox.KG_MORE_ANSWER)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Seed_type'))
async def callback_seed_type(callback: types.CallbackQuery):
    if callback.data == 'Seed_type1' or 'Seed_type2' or 'Seed_type3':
        await callback.message.reply(text='Какое количество кустов рассады вас интересует?',
                                     reply_markup=KeyBoards.ikb_volume_seed)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Seed_volume'))
async def callback_bush_value(callback: types.CallbackQuery):
    if callback.data == 'Seed_volume1':
        await callback.message.reply(text=MessageBox.BUSH_128_ANSWER)
    elif callback.data == 'Seed_volume2':
        await callback.message.reply(text=MessageBox.BUSH_256_ANSWER)
    elif callback.data == 'Seed_volume3':
        await callback.message.reply(text=MessageBox.BUSH_512_ANSWER)
    elif callback.data == 'Seed_more':
        await callback.message.reply(text=MessageBox.MORE_SEED_ANSWER)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
