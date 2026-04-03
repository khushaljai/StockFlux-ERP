# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import sqlite3
from typing import List, Dict, Any, Optional

DB_FILE = "price_tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            pack_size TEXT,
            units REAL,
            packaging TEXT,
            sku TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            date DATE NOT NULL,
            current_price REAL NOT NULL,
            wholesale_price REAL DEFAULT 0.0,
            market_price REAL DEFAULT 0.0,
            mrp REAL NOT NULL,
            quantity REAL,
            source TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)
    # create indices for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_id_date ON price_entries (product_id, date DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON price_entries (date DESC)")
    
    # Graceful Migration: Add wholesale_price if it doesn't exist
    try:
        cursor.execute("ALTER TABLE price_entries ADD COLUMN wholesale_price REAL DEFAULT 0.0")
    except sqlite3.OperationalError:
        pass # Column likely already exists
        
    try:
        cursor.execute("ALTER TABLE price_entries ADD COLUMN market_price REAL DEFAULT 0.0")
    except sqlite3.OperationalError:
        pass # Column likely already exists
    
    conn.commit()
    conn.close()

def execute_query(query: str, params: tuple = ()) -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def execute_write(query: str, params: tuple = ()) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def insert_many(query: str, params_list: List[tuple]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany(query, params_list)
    conn.commit()
    conn.close()
