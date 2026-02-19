import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "grab_helper.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Restaurants table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                rating REAL DEFAULT 4.5,
                cuisine_type TEXT,
                price_range TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Menus table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                menu_name TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            )
        ''')
        
        # Dishes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                dietary_tags TEXT,
                cuisine_type TEXT,
                ingredients TEXT,
                FOREIGN KEY (menu_id) REFERENCES menus(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_restaurant(self, name: str, rating: float = 4.5, cuisine_type: str = "", price_range: str = "medium") -> int:
        """Add a new restaurant to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO restaurants (name, rating, cuisine_type, price_range)
                VALUES (?, ?, ?, ?)
            ''', (name, rating, cuisine_type, price_range))
            conn.commit()
            restaurant_id = cursor.lastrowid
            conn.close()
            return restaurant_id
        except sqlite3.IntegrityError:
            conn.close()
            return self.get_restaurant_id(name)
    
    def get_restaurant_id(self, name: str) -> Optional[int]:
        """Get restaurant ID by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM restaurants WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def add_menu(self, restaurant_id: int, menu_name: str = "Main Menu") -> int:
        """Add a menu for a restaurant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO menus (restaurant_id, menu_name)
            VALUES (?, ?)
        ''', (restaurant_id, menu_name))
        conn.commit()
        menu_id = cursor.lastrowid
        conn.close()
        return menu_id
    
    def add_dish(self, menu_id: int, name: str, price: float, description: str = "", 
                 dietary_tags: str = "", cuisine_type: str = "", ingredients: str = ""):
        """Add a dish to a menu"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dishes (menu_id, name, price, description, dietary_tags, cuisine_type, ingredients)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (menu_id, name, price, description, dietary_tags, cuisine_type, ingredients))
        conn.commit()
        conn.close()
    
    def search_dishes(self, query: str, dietary_restrictions: List[str] = None, 
                     max_price: float = None) -> List[Dict]:
        """Search for dishes based on query and filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = '''
            SELECT d.id, d.name, d.price, d.description, d.dietary_tags, r.name as restaurant_name, r.rating
            FROM dishes d
            JOIN menus m ON d.menu_id = m.id
            JOIN restaurants r ON m.restaurant_id = r.id
            WHERE LOWER(d.name) LIKE ? OR LOWER(d.description) LIKE ? OR LOWER(d.ingredients) LIKE ?
        '''
        
        params = [f'%{query.lower()}%', f'%{query.lower()}%', f'%{query.lower()}%']
        
        # Add price filter
        if max_price:
            sql += ' AND d.price <= ?'
            params.append(max_price)
        
        # Add dietary restrictions filter
        if dietary_restrictions:
            dietary_conditions = ' OR '.join([f"d.dietary_tags LIKE ?" for _ in dietary_restrictions])
            sql += f' AND ({dietary_conditions})'
            params.extend([f'%{tag}%' for tag in dietary_restrictions])
        
        sql += ' ORDER BY r.rating DESC, d.price ASC'
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'name': r[1],
                'price': r[2],
                'description': r[3],
                'dietary_tags': r[4],
                'restaurant': r[5],
                'rating': r[6]
            }
            for r in results
        ]
    
    def get_all_dishes(self) -> List[Dict]:
        """Get all dishes from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.id, d.name, d.price, d.description, r.name, r.rating
            FROM dishes d
            JOIN menus m ON d.menu_id = m.id
            JOIN restaurants r ON m.restaurant_id = r.id
            ORDER BY r.rating DESC
        ''')
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'name': r[1],
                'price': r[2],
                'description': r[3],
                'restaurant': r[4],
                'rating': r[5]
            }
            for r in results
        ]
    
    def get_restaurants(self) -> List[Dict]:
        """Get all restaurants"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, rating, cuisine_type FROM restaurants ORDER BY rating DESC')
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'name': r[1],
                'rating': r[2],
                'cuisine_type': r[3]
            }
            for r in results
        ]
