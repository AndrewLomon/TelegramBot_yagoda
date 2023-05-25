import sqlite3
import time


class BotDB:
    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        print('Базза данных подключилась!')
        self.conn = sqlite3.connect((db_file))
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT id FROM clients WHERE user_id=?", (user_id,))
        return bool(len(result.fetchall()))

    def get_client_id(self, user_id):
        """Получаем id юзера в базе по его user_id в телеграмме"""
        result = self.cursor.execute("SELECT id FROM clients WHERE user_id=?", (user_id,))
        return result.fetchone()[0]


    def add_client(self, user_id, join_date, name, nick_name):
        """Добавляем клиента в БД"""
        self.cursor.execute("INSERT INTO clients ('user_id', 'join_date', 'name', 'nick_name') VALUES (?, ?, ?, ?)",
                            (user_id, join_date, name, nick_name))
        return self.conn.commit()

    def record_client_data(self, phone_number, adress, user_id):
        """Добавляем данные клиента"""
        self.cursor.execute("UPDATE clients SET phone_number = ?, adress = ? WHERE user_id = ?",
                            (phone_number, adress, user_id))
        return self.conn.commit()

    def record_order(self, user_id, product_type, product_subtype, volume_product, date):
        """Добавляем данные по заказу"""
        self.cursor.execute("INSERT INTO orders ('user_id', 'product_type', 'product_subtype', 'volume_product', 'date') VALUES (?, ?, ?, ?, ?)",
                            (user_id, product_type, product_subtype, volume_product, date))
        return self.conn.commit()
    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()

