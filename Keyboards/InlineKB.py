from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
                               callback_data='Seed_volume_more')
ikb_volume_seed.add(ikb_vs1,ikb_vs2,ikb_vs3).add(ikb_vs4)

#Клавиатура для запроса номера телефона
ikb_phone_number = InlineKeyboardMarkup(row_width=1)
ikb_phone = InlineKeyboardButton(text='Поделиться номером телефона',
                                 request_contact=True,
                                 callback_data='Phone')
ikb_phone_number.add(ikb_phone)

#Клавиатура для запроса номера локации
ikb_location_ask = InlineKeyboardMarkup(row_width=1)
ikb_location = InlineKeyboardButton(text='Поделиться расположением',
                                    request_location=True,
                                    callback_data='location')
ikb_location_ask.add(ikb_location)