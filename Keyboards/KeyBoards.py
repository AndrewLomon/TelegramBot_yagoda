from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3, resize_keyboard=True)
kb1 = KeyboardButton('/Make_order')
kb2 = KeyboardButton('/Discounts')
kb3 = KeyboardButton('/Cancel')
kb_main.add(kb1,kb2).insert(kb3)

