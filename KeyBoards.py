from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3, resize_keyboard=True)
kb1 = KeyboardButton('Клубника')
kb2 = KeyboardButton('Рассада')
kb_main.add(kb1,kb2)

#Клавиатура под сообщением с выбором товара (клубника или рассада)
ikb_order = InlineKeyboardMarkup(row_width=2)
ikb1 = InlineKeyboardButton(text='Клубника',
                            callback_data='Product1')
ikb2 = InlineKeyboardButton(text='Рассада',
                            callback_data='Product2')
ikb_order.add(ikb1,ikb2)

#Клавиатура для выбора объема товара клубники
ikb_Straw = InlineKeyboardMarkup(row_width=3)
ikb_S1 = InlineKeyboardButton(text='3 kg',
                              callback_data='value3')
ikb_S2 = InlineKeyboardButton(text='6 kg',
                              callback_data='value6')
ikb_S3 = InlineKeyboardButton(text='9 kg',
                              callback_data='value9')
ikb_S4 = InlineKeyboardButton(text='More',
                              callback_data='more')
ikb_Straw.add(ikb_S1,ikb_S2,ikb_S3).add(ikb_S4)

#Клавиатура для выбора сорта рассады
ikb_type_seed = InlineKeyboardMarkup(row_width=3)
ikb_ts1 = InlineKeyboardButton(text='Кабрилло',
                              callback_data='Seedtype1')
ikb_ts2 = InlineKeyboardButton(text='Мурано',
                              callback_data='Seedtype2')
ikb_ts3 = InlineKeyboardButton(text='Мара-де-буа',
                              callback_data='Seedtype3')
ikb_type_seed.add(ikb_ts1,ikb_ts2,ikb_ts3)