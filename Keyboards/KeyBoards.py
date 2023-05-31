from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
kb1 = KeyboardButton('Сделать заказ')
kb2 = KeyboardButton('Скидки')
kb3 = KeyboardButton('Отмена заказа')
kb_main.add(kb1).row(kb2, kb3)

#Админская клавиатура в чате
kb_admin = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
kb1 = KeyboardButton('Добавить админа')
kb2 = KeyboardButton('Удалить себя из рассылки')
kb3 = KeyboardButton('Выгрузить базу данных')
kb4 = KeyboardButton('Закрыть админку')
kb_admin.add(kb1, kb2, kb3).row(kb4)