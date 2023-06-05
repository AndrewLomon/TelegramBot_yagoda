from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import MessageBox
from Keyboards import InlineKB
from handlers.client import FSM_client



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

def register_handlers_callback(dp: Dispatcher):
    # TODO: Добавить для этих функций блок на повторное нажатия
    dp.register_callback_query_handler(callback_kg_value, state=FSM_client.volume_berry)

