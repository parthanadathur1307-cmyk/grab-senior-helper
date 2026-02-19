import sqlite3
import json
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name='grab_helper.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # Restaurants table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                rating REAL DEFAULT 0,
                cuisine_type TEXT,
                price_range TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Menus table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                menu_json TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
            )
        ''')
        
        # Dishes table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                dietary_tags TEXT,
                category TEXT,
                FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
            )
        ''')
        
        self.conn.commit()
    
    def add_restaurant(self, name: str, rating: float = 0, cuisine_type: str = "", price_range: str = ""):
        try:
            self.cursor.execute('''
                INSERT INTO restaurants (name, rating, cuisine_type, price_range)
                VALUES (?, ?, ?, ?)
            ''', (name, rating, cuisine_type, price_range))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_all_restaurants(self) -> List[Dict]:
        self.cursor.execute('SELECT * FROM restaurants')
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict]:
        self.cursor.execute('SELECT * FROM restaurants WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        if row:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, row))
        return None
    
    def add_dishes(self, restaurant_id: int, dishes: List[Dict]):
        for dish in dishes:
            dietary_tags = json.dumps(dish.get('dietary_tags', []))
            self.cursor.execute('''
                INSERT INTO dishes (restaurant_id, name, description, price, dietary_tags, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                restaurant_id,
                dish.get('name', ''),
                dish.get('description', ''),
                dish.get('price', 0),
                dietary_tags,
                dish.get('category', '')
            ))
        self.conn.commit()
    
    def get_dishes_by_restaurant(self, restaurant_id: int) -> List[Dict]:
        self.cursor.execute('SELECT * FROM dishes WHERE restaurant_id = ?', (restaurant_id,))
        columns = [description[0] for description in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            dish = dict(zip(columns, row))
            dish['dietary_tags'] = json.loads(dish['dietary_tags'])
            results.append(dish)
        return results
    
    def get_all_dishes(self) -> List[Dict]:
        self.cursor.execute('SELECT * FROM dishes')
        columns = [description[0] for description in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            dish = dict(zip(columns, row))
            dish['dietary_tags'] = json.loads(dish['dietary_tags'])
            results.append(dish)
        return results
    
    def close(self):
        self.conn.close()