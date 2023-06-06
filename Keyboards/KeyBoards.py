from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

#Общая клавиатура в чате
kb_main = ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2, resize_keyboard=True)
kb_main.row('Меню', 'Скидки').add('Сделать заказ 🍓').add('Отмена заказа ⭕️')

#Админская клавиатура в чате
kb_admin = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
kb1 = KeyboardButton('Добавить админа')
kb2 = KeyboardButton('Удалить себя из рассылки')
kb3 = KeyboardButton('Выгрузить базу данных')
kb4 = KeyboardButton('Обновить меню')
kb5 = KeyboardButton('Закрыть админку')
kb_admin.add(kb1, kb2).add(kb3, kb4).row(kb5)