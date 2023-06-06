import sqlite3



class BotDB:
    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect((db_file))
        print('Базза данных подключилась!')
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT id FROM clients WHERE user_id=?", (user_id,))
        return bool(len(result.fetchall()))

    def get_client_ID(self, user_id):
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

    def record_order(self, user_id, volume_product, date):
        """Добавляем данные по заказу"""
        self.cursor.execute("INSERT INTO orders ('user_id', 'volume_product', 'date') VALUES (?, ?, ?)",
                            (user_id, volume_product, date))
        return self.conn.commit()

    def get_client_info(self):
        query = "SELECT * FROM clients"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_client_orders(self, user_id):
        query = "SELECT volume_product, date FROM orders WHERE user_id=?"
        self.cursor.execute(query, (user_id,))
        data = self.cursor.fetchall()
        return data

    def admin_exists(self, user_id):
        """Проверяем, есть ли админ в БД"""
        result = self.cursor.execute("SELECT id FROM admins WHERE admin_id=?", (user_id,))
        return bool(len(result.fetchall()))

    def add_admin(self, user_id, admin_name, date):
        """Добавляем админа в БД"""
        self.cursor.execute("INSERT INTO admins ('admin_id', 'admin_name', 'date') VALUES (?, ?, ?)",
                            (user_id, admin_name, date))
        return self.conn.commit()

    def delete_admin(self, user_id,):
        """Удаляем админа из БД"""
        self.cursor.execute("DELETE FROM admins WHERE admin_id=?",
                            (user_id,))
        return self.conn.commit()

    def get_admin_id(self):
        """Берём айди всех админов"""
        query = "SELECT admin_id FROM admins"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def add_menu(self, photo, name, description):
        """Удаляем старые данные в меню и загружаем новые"""
        self.cursor.execute("INSERT INTO menu ('photo', 'name', 'description') VALUES (?, ?, ?)",
                            (photo, name, description))
        return self.conn.commit()

    def get_menu(self):
        """Удаляем старые данные в меню и загружаем новые"""
        query = "SELECT * FROM menu"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
