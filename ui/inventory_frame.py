# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk
from tkinter import ttk
from data_engine import DataEngine

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # --- Top Section: Cards & Alerts ---
        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.top_container.grid_columnconfigure(0, weight=2)
        self.top_container.grid_columnconfigure(1, weight=1)
        
        # Cards
        self.cards_frame = ctk.CTkFrame(self.top_container)
        self.cards_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.cards_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.card_total_prod = self.create_card(self.cards_frame, "Total Unique Products", "0", 0)
        self.card_asset_val = self.create_card(self.cards_frame, "Total Asset Value", "₹0.00", 1)
        
        # Low Stock Alerts
        self.alerts_frame = ctk.CTkFrame(self.top_container)
        self.alerts_frame.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(self.alerts_frame, text="Low Stock Alerts (< 10 units)", font=ctk.CTkFont(weight="bold", size=14), text_color="#A83232").pack(pady=(10, 5))
        
        # A small scrollable textbox for alerts
        self.alerts_text = ctk.CTkTextbox(self.alerts_frame, fg_color="transparent", height=60, font=ctk.CTkFont(size=12))
        self.alerts_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # --- Bottom Section: Master Catalog Grid ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.table_frame, text="Master Product Catalog & Pricing", font=ctk.CTkFont(weight="bold", size=16)).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        
        self.tree_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.tree_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree_container.grid_columnconfigure(0, weight=1)
        
        columns = ("Product", "Brand", "Pack Size", "Units", "Pkg Type", "Retail", "Wholesale", "Market", "MRP", "Stock Qty", "Total Value")
        self.tree = ttk.Treeview(self.tree_container, columns=columns, show="headings")
        
        # Define columns sizes appropriately
        col_widths = {
            "Product": 200, "Brand": 100, "Pack Size": 80, "Units": 60, "Pkg Type": 80,
            "Retail": 80, "Wholesale": 80, "Market": 80, "MRP": 80, 
            "Stock Qty": 80, "Total Value": 100
        }
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c, False))
            self.tree.column(col, width=col_widths.get(col, 100), anchor="center" if col != "Product" else "w")
            
        scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def create_card(self, parent, title, val, col):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, sticky="nsew", padx=10, pady=10)
        
        try:
            from .utils import enhance_card
            enhance_card(frame)
        except ImportError:
            pass
            
        lbl_title = ctk.CTkLabel(frame, text=title, text_color="#A0A0A0", font=ctk.CTkFont(size=14))
        lbl_title.pack(pady=(20, 5))
        lbl_val = ctk.CTkLabel(frame, text=val, font=ctk.CTkFont(size=36, weight="bold"), text_color="#FFFFFF")
        lbl_val.pack(pady=(0, 20))
        lbl_val._current_val = 0.0
        return lbl_val

    def refresh_data(self):
        snapshots = DataEngine.get_all_snapshots()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        total_asset_value = 0.0
        alerts = []
        
        for snap in snapshots:
            qty = float(snap.get('quantity') or 0.0)
            wholesale = float(snap.get('wholesale_price') or 0.0)
            
            value = qty * wholesale
            total_asset_value += value
            
            # Low stock check
            product_name = snap.get('name', 'Unknown')
            if qty < 10.0:
                alerts.append(f"⚠️ {product_name} ({qty} units remaining)")
            
            # Insert into tree
            self.tree.insert("", "end", values=(
                product_name,
                snap.get('brand', ''),
                snap.get('pack_size', ''),
                snap.get('units', 1.0),
                snap.get('packaging', ''),
                f"₹{snap.get('current_price', 0)}",
                f"₹{wholesale}",
                f"₹{snap.get('market_price', 0)}",
                f"₹{snap.get('mrp', 0)}",
                qty,
                f"₹{value:,.2f}"
            ))
            
        # Update Cards
        from .utils import animate_number
        animate_number(self.card_total_prod, getattr(self.card_total_prod, '_current_val', 0.0), float(len(snapshots)), is_float=False)
        self.card_total_prod._current_val = float(len(snapshots))
        
        animate_number(self.card_asset_val, getattr(self.card_asset_val, '_current_val', 0.0), total_asset_value, prefix="₹")
        self.card_asset_val._current_val = total_asset_value
        
        # Update Alerts
        self.alerts_text.configure(state="normal")
        self.alerts_text.delete("1.0", "end")
        if not alerts:
            self.alerts_text.insert("1.0", "✅ All stock levels are healthy! (>10 units)")
        else:
            self.alerts_text.insert("1.0", "\n".join(alerts))
        self.alerts_text.configure(state="disabled")

    def sort_treeview(self, col, reverse):
        # A simple sort method for the master grid
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        try:
            # Try numeric sort by stripping ₹ and commas
            l.sort(key=lambda t: float(t[0].replace('₹', '').replace(',', '')), reverse=reverse)
        except ValueError:
            # Fallback to string sort
            l.sort(reverse=reverse)
            
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
            
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))
