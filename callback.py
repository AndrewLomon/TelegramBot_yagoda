from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import MessageBox
from Keyboards import InlineKB
from create_bot import dp
from handlers.client import FSM_client


async def callback_make_order(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(start_order=cb)
    print(await state.get_data())
    if cb == 'Клубника':
        await callback.message.reply(text='Сколько килограм вы хотите заказать?',
                                     reply_markup=InlineKB.ikb_Straw)
        await FSM_client.type_product.set()
    elif cb == 'Рассада':
        await callback.message.reply(text='Какой сорт вас интересует?',
                                     reply_markup=InlineKB.ikb_type_seed)
        await FSM_client.sub_type_product.set()


async def callback_kg_value(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(type_product=cb)
    if cb == 'value_more':
        await callback.message.reply(text=MessageBox.KG_MORE_ANSWER)
        await FSM_client.extra_volume_product.set()
    else:
        if cb == '3кг':
            await callback.message.reply(text=MessageBox.KG3_ANSWER)
        elif cb == '6кг':
            await callback.message.reply(text=MessageBox.KG6_ANSWER)
        elif cb == '9кг':
            await callback.message.reply(text=MessageBox.KG9_ANSWER)
        await FSM_client.client_location.set()




async def callback_seed_type(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(sub_type_product=cb)
    if callback.data == 'Кабрилло' or 'Мурано' or 'Мара-де-буа':
        await callback.message.reply(text='Какое количество кустов рассады вас интересует?',
                                     reply_markup=InlineKB.ikb_volume_seed)
    await FSM_client.volume_product.set()


async def callback_bush_value(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(volume_product=cb)
    if cb == 'Seed_volume_more':
        await callback.message.reply(text=MessageBox.MORE_SEED_ANSWER)
        await FSM_client.extra_volume_product.set()
    else:
        if callback.data == '128_кустов':
            await callback.message.reply(text=MessageBox.BUSH_128_ANSWER)
        elif callback.data == '256_кустов':
            await callback.message.reply(text=MessageBox.BUSH_256_ANSWER)
        elif callback.data == '512_кустов':
            await callback.message.reply(text=MessageBox.BUSH_512_ANSWER)
        await FSM_client.client_location.set()

def register_handlers_callback(dp: Dispatcher):
    # TODO: Добавить для этих функций блок на повторное нажатие
    dp.register_callback_query_handler(callback_make_order, state=FSM_client.start_order)
    dp.register_callback_query_handler(callback_kg_value, state=FSM_client.type_product)
    dp.register_callback_query_handler(callback_seed_type, state=FSM_client.sub_type_product)
    dp.register_callback_query_handler(callback_bush_value, state=FSM_client.volume_product)
