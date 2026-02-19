import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path="senior_helper.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Restaurants table
        cursor.execute('''
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                name TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            )
        ''')

        # Dishes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                menu_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                dietary_tags TEXT,
                ingredients TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
                FOREIGN KEY (menu_id) REFERENCES menus(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_restaurant(self, name: str, rating: float = 0, cuisine_type: str = "", price_range: str = ""):
        """Add a new restaurant"""
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
            return None

    def add_dish(self, restaurant_id: int, name: str, description: str = "", price: float = 0, 
                 dietary_tags: str = "", ingredients: str = "", menu_id: int = None):
        """Add a dish to a restaurant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dishes (restaurant_id, menu_id, name, description, price, dietary_tags, ingredients)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (restaurant_id, menu_id, name, description, price, dietary_tags, ingredients))
        conn.commit()
        dish_id = cursor.lastrowid
        conn.close()
        return dish_id

    def search_dishes(self, query: str, dietary_restrictions: List[str] = None, max_price: float = None) -> List[Dict]:
        """Search dishes by name, description, or ingredients with filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build the query
        sql = '''
            SELECT d.id, d.name, d.description, d.price, d.dietary_tags, 
                   r.name as restaurant_name, r.rating
            FROM dishes d
            JOIN restaurants r ON d.restaurant_id = r.id
            WHERE (d.name LIKE ? OR d.description LIKE ? OR d.ingredients LIKE ?)
        '''
        params = [f"%{query}%, f"%{query}%, f"%{query}%"]

        # Add price filter
        if max_price is not None:
            sql += " AND d.price <= ?"
            params.append(max_price)

        # Add dietary restrictions filter
        if dietary_restrictions:
            for restriction in dietary_restrictions:
                sql += f" AND d.dietary_tags NOT LIKE ?"
                params.append(f"%{restriction}%")

        sql += " ORDER BY r.rating DESC"

        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()

        dishes = []
        for row in results:
            dishes.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'dietary_tags': row[4],
                'restaurant_name': row[5],
                'rating': row[6]
            })

        return dishes

    def get_all_restaurants(self) -> List[Dict]:
        """Get all restaurants from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, rating, cuisine_type, price_range FROM restaurants ORDER BY rating DESC')
        results = cursor.fetchall()
        conn.close()

        restaurants = []
        for row in results:
            restaurants.append({
                'id': row[0],
                'name': row[1],
                'rating': row[2],
                'cuisine_type': row[3],
                'price_range': row[4]
            })
        return restaurants

    def get_restaurant_dishes(self, restaurant_id: int) -> List[Dict]:
        """Get all dishes for a specific restaurant"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, description, price, dietary_tags
            FROM dishes
            WHERE restaurant_id = ?
            ORDER BY name
        ''', (restaurant_id,))
        results = cursor.fetchall()
        conn.close()

        dishes = []
        for row in results:
            dishes.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'dietary_tags': row[4]
            })
        return dishes
