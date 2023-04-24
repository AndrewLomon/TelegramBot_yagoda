from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3, resize_keyboard=True)
kb1 = KeyboardButton('/Make_order')
kb2 = KeyboardButton('/Discounts')
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
ikb_S4 = InlineKeyboardButton(text='Заказать больше',
                              callback_data='value_more')
ikb_Straw.add(ikb_S1,ikb_S2,ikb_S3).add(ikb_S4)

#Клавиатура для выбора сорта рассады
ikb_type_seed = InlineKeyboardMarkup(row_width=3)
ikb_ts1 = InlineKeyboardButton(text='Кабрилло',
                               callback_data='Seed_type1')
ikb_ts2 = InlineKeyboardButton(text='Мурано',
                               callback_data='Seed_type2')
ikb_ts3 = InlineKeyboardButton(text='Мара-де-буа',
                               callback_data='Seed_type3')
ikb_type_seed.add(ikb_ts1,ikb_ts2,ikb_ts3)

#Клавиатура для выбора количества кустов рассады
ikb_volume_seed = InlineKeyboardMarkup(row_width=3)
ikb_vs1 = InlineKeyboardButton(text='128 кустов',
                               callback_data='Seed_volume1')
ikb_vs2 = InlineKeyboardButton(text='256 кустов',
                               callback_data='Seed_volume2')
ikb_vs3 = InlineKeyboardButton(text='512 кустов',
                               callback_data='Seed_volume3')
ikb_vs4 = InlineKeyboardButton(text='Свой вариант количества кустов',
                               callback_data='Seed_more')
ikb_volume_seed.add(ikb_vs1,ikb_vs2,ikb_vs3).add(ikb_vs4)
