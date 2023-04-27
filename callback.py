from aiogram import types, Dispatcher
from create_bot import dp
import MessageBox
from Keyboards import KeyBoards, InlineKB
from handlers.client import FSMСlient
from aiogram.dispatcher import FSMContext



@dp.callback_query_handler(state=FSMСlient.start_order)
async def callback_make_order(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(start_order=cb)
    print(await state.get_data())
    if cb == 'Product1':
        await callback.message.reply(text='Сколько килограм вы хотите заказать?',
                                     reply_markup=InlineKB.ikb_Straw)
        await FSMСlient.type_product.set()
    elif cb == 'Product2':
        await callback.message.reply(text='Какой сорт вас интересует?',
                                     reply_markup=InlineKB.ikb_type_seed)
        await FSMСlient.sub_type_product.set()


@dp.callback_query_handler(state=FSMСlient.type_product)
async def callback_kg_value(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(type_product=cb)
    print(await state.get_data())
    if cb == 'value3':
        await callback.message.reply(text=MessageBox.KG3_ANSWER)
    elif cb == 'value6':
        await callback.message.reply(text=MessageBox.KG6_ANSWER)
    elif cb == 'value9':
        await callback.message.reply(text=MessageBox.KG9_ANSWER)
    elif cb == 'value_more':
        await callback.message.reply(text=MessageBox.KG_MORE_ANSWER)
    # await FSMСlient.next()

@dp.callback_query_handler(state=FSMСlient.sub_type_product)
async def callback_seed_type(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(sub_type_product=cb)
    print(await state.get_data())
    if callback.data == 'Seed_type1' or 'Seed_type2' or 'Seed_type3':
        await callback.message.reply(text='Какое количество кустов рассады вас интересует?',
                                     reply_markup=InlineKB.ikb_volume_seed)
    await FSMСlient.volume_product.set()


@dp.callback_query_handler(state=FSMСlient.volume_product)
async def callback_bush_value(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(volume_product=cb)
    print(await state.get_data())
    if callback.data == 'Seed_volume1':
        await callback.message.reply(text=MessageBox.BUSH_128_ANSWER)
    elif callback.data == 'Seed_volume2':
        await callback.message.reply(text=MessageBox.BUSH_256_ANSWER)
    elif callback.data == 'Seed_volume3':
        await callback.message.reply(text=MessageBox.BUSH_512_ANSWER)
    elif callback.data == 'Seed_volume_more':
        await callback.message.reply(text=MessageBox.MORE_SEED_ANSWER)
    await FSMСlient.next()



# def register_handlers_callback(dp: Dispatcher):
#     dp.register_callback_query_handler(callback_make_order, lambda x: x.data and x.data.startswith('Product'), state=FSMСlient.start_order)