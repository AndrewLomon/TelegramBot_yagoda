from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2, resize_keyboard=True)
kb_main.row('Меню', 'Скидки').add('Сделать заказ 🍓').add('Отмена заказа ⭕️')

#Админская клавиатура в чате
kb_admin = ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2, resize_keyboard=True)
kb1 = KeyboardButton('Добавить себя в рассылку')
kb2 = KeyboardButton('Удалить себя из рассылки')
kb3 = KeyboardButton('БД')
kb4 = KeyboardButton('Закрыть админку')
kb_admin.add(kb1, kb2).add(kb3).row(kb4)

#Админская клавиатура управления БД
kb_db = ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2, resize_keyboard=True)
kb_db.add('Обновить меню', 'Удалить опции в меню').add('Выгрузить заказы').add('Вернуться в админку')
