# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

from typing import List, Dict, Any
from database import execute_query

class DataEngine:
    @staticmethod
    def get_all_products() -> List[Dict[str, Any]]:
        query = "SELECT * FROM products ORDER BY name ASC"
        rows = execute_query(query)
        return [dict(row) for row in rows]

    @staticmethod
    def get_product_by_id(product_id: int) -> Dict[str, Any]:
        query = "SELECT * FROM products WHERE id = ?"
        rows = execute_query(query, (product_id,))
        return dict(rows[0]) if rows else {}
        
    @staticmethod
    def get_latest_snapshot(product_id: int) -> Dict[str, Any]:
        """
        The CORE REQUIREMENT: Latest Snapshot Engine
        Equivalent of Excel logic: "Give me the latest row for this product with all columns"
        """
        query = """
            SELECT p.*, pe.date, pe.current_price, pe.wholesale_price, pe.market_price, pe.mrp, pe.quantity, pe.source, (pe.market_price - pe.wholesale_price) as price_diff
            FROM products p
            LEFT JOIN price_entries pe ON p.id = pe.product_id
            WHERE p.id = ?
            ORDER BY pe.date DESC
            LIMIT 1
        """
        rows = execute_query(query, (product_id,))
        return dict(rows[0]) if rows else {}

    @staticmethod
    def get_price_history(product_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT * FROM price_entries 
            WHERE product_id = ? 
            ORDER BY date DESC
        """
        rows = execute_query(query, (product_id,))
        return [dict(row) for row in rows]
        
    @staticmethod
    def get_all_snapshots() -> List[Dict[str, Any]]:
        query = """
            SELECT p.id as product_id, p.name, p.brand, p.pack_size, p.units, p.packaging, p.sku, 
                   pe.date, pe.current_price, pe.wholesale_price, pe.market_price, pe.mrp, pe.quantity, pe.source, (pe.market_price - pe.wholesale_price) as price_diff
            FROM products p
            LEFT JOIN (
                SELECT product_id, MAX(date) as max_date
                FROM price_entries
                GROUP BY product_id
            ) latest ON p.id = latest.product_id
            LEFT JOIN price_entries pe ON p.id = pe.product_id AND pe.date = latest.max_date
            ORDER BY p.name ASC
        """
        rows = execute_query(query)
        return [dict(row) for row in rows]

    @staticmethod
    def get_full_price_history() -> List[Dict[str, Any]]:
        query = """
            SELECT p.name as product_name, p.brand, pe.date, pe.current_price, pe.wholesale_price, pe.market_price, pe.mrp, pe.quantity, pe.source
            FROM price_entries pe
            JOIN products p ON p.id = pe.product_id
            ORDER BY pe.date DESC, p.name ASC
        """
        rows = execute_query(query)
        return [dict(row) for row in rows]
        
    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        """Gets some global stats if nothing is selected"""
        query_total_products = "SELECT COUNT(*) as cnt FROM products"
        query_latest_entry = "SELECT MAX(date) as max_date FROM price_entries"
        
        total_prods = execute_query(query_total_products)[0]['cnt']
        latest_date = execute_query(query_latest_entry)[0]['max_date']
        
        return {
            "total_products": total_prods,
            "last_updated": latest_date
        }

    @staticmethod
    def update_product(product_id: int, name: str, brand: str, pack_size: str, units: float, packaging: str, sku: str) -> bool:
        from database import execute_write
        query = "UPDATE products SET name=?, brand=?, pack_size=?, units=?, packaging=?, sku=? WHERE id=?"
        execute_write(query, (name, brand, pack_size, units, packaging, sku, product_id))
        return True

    @staticmethod
    def add_new_product(name: str, brand: str, pack_size: str, units: float, packaging: str, sku: str) -> int:
        from database import execute_write
        query = "INSERT INTO products (name, brand, pack_size, units, packaging, sku) VALUES (?, ?, ?, ?, ?, ?)"
        return execute_write(query, (name, brand, pack_size, units, packaging, sku))

    @staticmethod
    def add_price_entry(product_id: int, entry_date: str, price: float, wholesale_price: float, market_price: float, mrp: float, quantity: float, source: str = "Manual") -> int:
        from database import execute_write
        query = "INSERT INTO price_entries (product_id, date, current_price, wholesale_price, market_price, mrp, quantity, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        return execute_write(query, (product_id, entry_date, price, wholesale_price, market_price, mrp, quantity, source))
