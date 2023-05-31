from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import MessageBox
from Keyboards import InlineKB
from handlers.client import FSM_client

async def callback_make_order(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    await state.update_data(type_product=cb)
    if cb == 'Клубника':
        await callback.message.reply(text='Сколько килограм вы хотите заказать?',
                                     reply_markup=InlineKB.ikb_Straw)
        await FSM_client.volume_berry.set()
        await callback.message.delete()
    elif cb == 'Рассада':
        await callback.message.reply(text='Какой сорт вас интересует?',
                                     reply_markup=InlineKB.ikb_type_seed)
        await FSM_client.sub_type_product.set()
        await callback.message.delete()
    else:
        await callback.answer('Вы уже выбрали продукт.', show_alert=True)


async def callback_kg_value(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    if cb == 'value_more':
        await callback.message.reply(text=MessageBox.KG_MORE_ANSWER)
        await callback.message.delete()
    else:
        await state.update_data(volume_berry=cb)
        if cb == '3кг':
            await callback.message.reply(text=MessageBox.KG3_ANSWER,
                                         parse_mode='html')
        elif cb == '6кг':
            await callback.message.reply(text=MessageBox.KG6_ANSWER,
                                         parse_mode='html')
        elif cb == '9кг':
            await callback.message.reply(text=MessageBox.KG9_ANSWER,
                                         parse_mode='html')
        await FSM_client.client_location.set()
        await callback.message.delete()



async def callback_seed_type(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    if callback.data == 'Кабрилло' or 'Мурано' or 'Мара-де-буа':
        await state.update_data(sub_type_product=cb)
        await callback.message.reply(text='Какое количество кустов рассады вас интересует?',
                                     reply_markup=InlineKB.ikb_volume_seed)
        await FSM_client.volume_bush.set()
        await callback.message.delete()
    else:
        await callback.answer('Что-то не так с заказом типа рассады', show_alert=True)


async def callback_bush_value(callback: types.CallbackQuery, state: FSMContext):
    cb = callback.data
    if cb == 'Seed_volume_more':
        await callback.message.reply(text=MessageBox.MORE_SEED_ANSWER)
        await callback.message.delete()
    else:
        await state.update_data(volume_bush=cb)
        if callback.data == '128_кустов':
            await callback.message.reply(text=MessageBox.BUSH_128_ANSWER,
                                         parse_mode='html')
        elif callback.data == '256_кустов':
            await callback.message.reply(text=MessageBox.BUSH_256_ANSWER,
                                         parse_mode='html')
        elif callback.data == '512_кустов':
            await callback.message.reply(text=MessageBox.BUSH_512_ANSWER,
                                         parse_mode='html')
        await FSM_client.client_location.set()
        await callback.message.delete()

def register_handlers_callback(dp: Dispatcher):
    # TODO: Добавить для этих функций блок на повторное нажатия
    dp.register_callback_query_handler(callback_make_order, state=FSM_client.type_product)
    dp.register_callback_query_handler(callback_bush_value, state=FSM_client.volume_bush)
    dp.register_callback_query_handler(callback_kg_value, state=FSM_client.volume_berry)
    dp.register_callback_query_handler(callback_seed_type, state=FSM_client.sub_type_product)

