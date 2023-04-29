from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
kb1 = KeyboardButton('Заказать')
kb2 = KeyboardButton('Скидки')
kb3 = KeyboardButton('Отмена')
kb_main.add(kb1).row(kb2,kb3)

