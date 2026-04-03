# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import pandas as pd
import random
from datetime import datetime, timedelta

def create_mock_csv():
    products = [
        {"Brand": "Nestle", "Product Name": "Maggi Noodles", "Pack Size": "70g", "Units": 1, "Packaging": "Packet", "SKU": "NES-MAG-70"},
        {"Brand": "Cadbury", "Product Name": "Dairy Milk", "Pack Size": "50g", "Units": 1, "Packaging": "Wrapper", "SKU": "CAD-DM-50"},
        {"Brand": "Tata", "Product Name": "Tata Salt", "Pack Size": "1kg", "Units": 1, "Packaging": "Packet", "SKU": "TAT-SAL-1"},
    ]
    
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for _ in range(50):
        prod = random.choice(products)
        days_offset = random.randint(0, 30)
        entry_date = base_date + timedelta(days=days_offset)
        
        mrp = random.choice([14.0, 20.0, 25.0])
        price = mrp - random.uniform(0, 3.0)
        
        row = {
            "Date": entry_date.strftime("%Y-%m-%d"),
            "Brand": prod["Brand"],
            "Product Name": prod["Product Name"],
            "Pack Size": prod["Pack Size"],
            "Units": prod["Units"],
            "Packaging": prod["Packaging"],
            "SKU": prod["SKU"],
            "MRP": round(mrp, 2),
            "Price": round(price, 2),
            "Quantity": random.randint(10, 100)
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    df.to_csv("mock_busy_data.csv", index=False)
    print("Created mock_busy_data.csv with", len(df), "rows.")

if __name__ == "__main__":
    create_mock_csv()
