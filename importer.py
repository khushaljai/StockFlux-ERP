# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import pandas as pd
from datetime import datetime
from database import execute_write, execute_query
import math

def clean_string(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def get_val(row_dict, keys: list, default=None):
    for k in keys:
        if k in row_dict and not pd.isna(row_dict[k]):
            return row_dict[k]
    return default

def import_csv(filepath: str, source: str) -> dict:
    """
    Imports a CSV or Excel file from Busy or Stocky.
    Includes custom mappings for Edible Oil Tracker format.
    """
    try:
        if filepath.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
        
        # apply cleaning to object columns
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(clean_string)
                
        added_products = 0
        added_entries = 0
        
        for _, row in df.iterrows():
            # Create a lowercase standardized dictionary of the row
            row_dict = {str(k).strip().lower(): v for k, v in row.to_dict().items()}
            
            # --- PRODUCT MAPPING ---
            # the excel has both "Product Name" and "product name", we check standard keys
            p_name = get_val(row_dict, ['product name', 'item name', 'name'], 'Unknown Product')
            p_brand = get_val(row_dict, ['brand', 'brand name'], '')
            p_sku = get_val(row_dict, ['sku', 'item code'], '')
            
            # pack size logic: e.g. "15 L" or "13 Kg"
            ps_val = get_val(row_dict, ['pack size', 'pack_size'], '')
            unit_val = get_val(row_dict, ['units', 'unit'], '')
            p_pack_size = f"{ps_val} {unit_val}".strip() if ps_val else ""

            # units (numeric)
            p_units_raw = get_val(row_dict, ['cartoon size', 'carton size', 'units_num'], 1.0)
            try:
                p_units = float(p_units_raw)
            except:
                p_units = 1.0

            # packaging type
            p_packaging = str(get_val(row_dict, ['packaging', 'package_type'], ''))
            # in some sheets Quantity is actually a unit like 'pcs'
            if not p_packaging:
                qty_val = get_val(row_dict, ['quantity', 'qty'], '')
                if isinstance(qty_val, str) and not qty_val.isnumeric():
                    p_packaging = qty_val

            # Find or insert product
            p_query = "SELECT id FROM products WHERE name = ?"
            res = execute_query(p_query, (p_name,))
            if res:
                product_id = res[0]['id']
            else:
                product_id = execute_write(
                    "INSERT INTO products (name, brand, pack_size, units, packaging, sku) VALUES (?, ?, ?, ?, ?, ?)",
                    (p_name, p_brand, p_pack_size, p_units, p_packaging, p_sku)
                )
                added_products += 1

            # --- PRICE ENTRY MAPPING ---
            # Date
            raw_date = get_val(row_dict, ['date', 'entry_date'], datetime.now())
            try:
                dt = pd.to_datetime(raw_date).strftime('%Y-%m-%d')
            except:
                dt = datetime.now().strftime('%Y-%m-%d')
                
            # Retail Price (we remove 'market price' so it doesn't cross over)
            p_price = float(get_val(row_dict, ['retail price', 'retail_price', 'current_price', 'price', 'rate', 'retail'], 0.0))
            
            # Market Price (Competitor benchmark)
            p_mprice = float(get_val(row_dict, ['current market price', 'market price', 'market_price', 'market rate', 'competitor price'], 0.0))
            
            # Wholesale Price
            p_wprice = float(get_val(row_dict, ['wholesale price', 'wholesale', 'bulk price', 'b2b price', 'wholesale_price', 'wholesale rate'], 0.0))
            
            # MRP
            p_mrp = float(get_val(row_dict, ['mrp per piece', 'mrp per cartoon', 'mrp'], 0.0))
            
            # Quantity (Inventory count)
            # Prioritize 'actual quantity' for standard sheets, then fallback to 'quantity'
            inv_qty_raw = get_val(row_dict, ['actual quantity', 'inventory', 'stock', 'quantity', 'qty'], 0.0)
            try:
                p_inv_qty = float(inv_qty_raw)
            except:
                p_inv_qty = 0.0
                
            # Source (Prioritize file's column if exists, otherwise fallback to dropdown choice)
            p_source = str(get_val(row_dict, ['source', 'origin'], source)).strip()
            if not p_source or pd.isna(p_source) or p_source.lower() == 'nan':
                p_source = source
                
            execute_write(
                "INSERT INTO price_entries (product_id, date, current_price, wholesale_price, market_price, mrp, quantity, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (product_id, dt, p_price, p_wprice, p_mprice, p_mrp, p_inv_qty, p_source)
            )
            added_entries += 1
            
        return {"status": "success", "added_products": added_products, "added_entries": added_entries}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
