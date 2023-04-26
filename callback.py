from aiogram import types, Dispatcher
from create_bot import dp
import MessageBox
from Keyboards import KeyBoards, InlineKB



@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Product'))
async def callback_make_order(callback: types.CallbackQuery):
    if callback.data == 'Product1':
        await callback.message.reply(text='Сколько килограм вы хотите заказать?',
                                     reply_markup=InlineKB.ikb_Straw)
    elif callback.data == 'Product2':
        await callback.message.reply(text='Какой сорт вас интересует?',
                                     reply_markup=InlineKB.ikb_type_seed)

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
                                     reply_markup=InlineKB.ikb_volume_seed)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Seed_volume'))
async def callback_bush_value(callback: types.CallbackQuery):
    if callback.data == 'Seed_volume1':
        await callback.message.reply(text=MessageBox.BUSH_128_ANSWER)
    elif callback.data == 'Seed_volume2':
        await callback.message.reply(text=MessageBox.BUSH_256_ANSWER)
    elif callback.data == 'Seed_volume3':
        await callback.message.reply(text=MessageBox.BUSH_512_ANSWER)
    elif callback.data == 'Seed_volume_more':
        await callback.message.reply(text=MessageBox.MORE_SEED_ANSWER)
