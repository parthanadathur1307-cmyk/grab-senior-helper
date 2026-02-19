import sqlite3

class Database:
    def __init__(self, db_name='restaurants.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS restaurants (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                location TEXT NOT NULL);''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS menus (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                restaurant_id INTEGER,
                                name TEXT NOT NULL,
                                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id));''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                menu_id INTEGER,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                FOREIGN KEY (menu_id) REFERENCES menus(id));''')
        self.connection.commit()

    def add_restaurant(self, name, location):
        self.cursor.execute('INSERT INTO restaurants (name, location) VALUES (?, ?)', (name, location))
        self.connection.commit()

    def add_menu(self, restaurant_id, menu_name):
        self.cursor.execute('INSERT INTO menus (restaurant_id, name) VALUES (?, ?)', (restaurant_id, menu_name))
        self.connection.commit()

    def add_dish(self, menu_id, dish_name, price):
        self.cursor.execute('INSERT INTO dishes (menu_id, name, price) VALUES (?, ?, ?)', (menu_id, dish_name, price))
        self.connection.commit()

    def close(self):
        self.connection.close()