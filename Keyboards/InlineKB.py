from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Клавиатура для выбора объема товара клубники
ikb_Straw = InlineKeyboardMarkup(row_width=3)
ikb_S1 = InlineKeyboardButton(text='3 kg',
                              callback_data='3кг')
ikb_S2 = InlineKeyboardButton(text='6 kg',
                              callback_data='6кг')
ikb_S3 = InlineKeyboardButton(text='9 kg',
                              callback_data='9кг')
ikb_S4 = InlineKeyboardButton(text='Заказать больше',
                              callback_data='value_more')
ikb_Straw.add(ikb_S1, ikb_S2, ikb_S3).add(ikb_S4)



# Клавиатура для запроса номера телефона
ikb_phone_number = InlineKeyboardMarkup(row_width=1)
ikb_phone = InlineKeyboardButton(text='Поделиться номером телефона',
                                 request_contact=True,
                                 callback_data='Phone')
ikb_phone_number.add(ikb_phone)

# Клавиатура для запроса номера локации
ikb_location_ask = InlineKeyboardMarkup(row_width=1)
ikb_location = InlineKeyboardButton(text='Поделиться расположением',
                                    request_location=True,
                                    callback_data='location')
ikb_location_ask.add(ikb_location)
