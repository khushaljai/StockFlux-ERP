# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Product:
    id: Optional[int]
    name: str
    brand: str
    pack_size: str
    units: float
    packaging: str
    sku: str

@dataclass
class PriceEntry:
    id: Optional[int]
    product_id: int
    date: date
    current_price: float
    mrp: float
    quantity: float
    source: str
