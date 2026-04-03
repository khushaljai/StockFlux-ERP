# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from data_engine import DataEngine

class AddEntryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Manual Entry Form", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        # Tabview for New Product / Add Price
        self.tabview = ctk.CTkTabview(self, width=600)
        self.tabview.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.tabview.add("Update Price Entry")
        self.tabview.add("Create New Product")
        self.tabview.add("Edit Product")
        self.tabview.set("Update Price Entry")
        
        self.setup_price_tab()
        self.setup_product_tab()
        self.setup_edit_tab()

    def load_products(self):
        self.all_products = DataEngine.get_all_products()
        values = [f"{p['id']} - {p['name']} ({p['brand']})" for p in self.all_products]
        if not values:
            values = ["No products found"]
        self.p_selector.configure(values=values)
        if hasattr(self, 'edit_p_selector'):
            self.edit_p_selector.configure(values=values)
            
        if values and self.product_var.get() not in values and values[0] != "No products found":
            self.product_var.set(values[0])
            if hasattr(self, 'edit_product_var'):
                self.edit_product_var.set(values[0])
                self.on_edit_product_select(values[0])

    def setup_price_tab(self):
        tab = self.tabview.tab("Update Price Entry")
        tab.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(tab, text="Select Product:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.product_var = ctk.StringVar()
        self.p_selector = ctk.CTkOptionMenu(tab, variable=self.product_var, values=["Loading..."])
        self.p_selector.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = ctk.CTkEntry(tab, placeholder_text="e.g. 2026-04-03")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Retail Price:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.price_entry = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.price_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Wholesale Price:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.wprice_entry = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.wprice_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Market Price:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.mprice_entry = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.mprice_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="MRP:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.mrp_entry = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.mrp_entry.grid(row=5, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Quantity/Stock:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.qty_entry = ctk.CTkEntry(tab, placeholder_text="1.0")
        self.qty_entry.insert(0, "1.0")
        self.qty_entry.grid(row=6, column=1, padx=10, pady=10, sticky="we")
        
        self.submit_price_btn = ctk.CTkButton(tab, text="Log Price Entry", command=self.save_price)
        self.submit_price_btn.grid(row=7, column=0, columnspan=2, pady=20)

    def setup_product_tab(self):
        tab = self.tabview.tab("Create New Product")
        tab.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(tab, text="Product Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.pn_entry = ctk.CTkEntry(tab)
        self.pn_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Brand:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.pb_entry = ctk.CTkEntry(tab)
        self.pb_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Pack Size (e.g. 15 L):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.ps_entry = ctk.CTkEntry(tab)
        self.ps_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Units (Number):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.pu_entry = ctk.CTkEntry(tab)
        self.pu_entry.insert(0, "1.0")
        self.pu_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Package Type (e.g. pcs, bottle):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.ppt_entry = ctk.CTkEntry(tab)
        self.ppt_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")

        ctk.CTkLabel(tab, text="SKU/Barcode:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.psku_entry = ctk.CTkEntry(tab)
        self.psku_entry.grid(row=5, column=1, padx=10, pady=10, sticky="we")

        ctk.CTkLabel(tab, text="Retail Price:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.pn_rprice = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.pn_rprice.grid(row=6, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Wholesale Price:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.pn_wprice = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.pn_wprice.grid(row=7, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Market Price:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.pn_mprice = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.pn_mprice.grid(row=8, column=1, padx=10, pady=10, sticky="we")

        ctk.CTkLabel(tab, text="MRP:").grid(row=9, column=0, padx=10, pady=10, sticky="w")
        self.pn_mrp = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.pn_mrp.grid(row=9, column=1, padx=10, pady=10, sticky="we")
        
        self.submit_prod_btn = ctk.CTkButton(tab, text="Create Product", command=self.save_product)
        self.submit_prod_btn.grid(row=10, column=0, columnspan=2, pady=20)

    def setup_edit_tab(self):
        tab = self.tabview.tab("Edit Product")
        tab.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(tab, text="Select Product:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.edit_product_var = ctk.StringVar()
        self.edit_p_selector = ctk.CTkOptionMenu(tab, variable=self.edit_product_var, values=["Loading..."], command=self.on_edit_product_select)
        self.edit_p_selector.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Product Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.epn_entry = ctk.CTkEntry(tab)
        self.epn_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Brand:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.epb_entry = ctk.CTkEntry(tab)
        self.epb_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Pack Size:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.eps_entry = ctk.CTkEntry(tab)
        self.eps_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Units:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.epu_entry = ctk.CTkEntry(tab)
        self.epu_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Package Type:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.eppt_entry = ctk.CTkEntry(tab)
        self.eppt_entry.grid(row=5, column=1, padx=10, pady=10, sticky="we")

        ctk.CTkLabel(tab, text="SKU/Barcode:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.epsku_entry = ctk.CTkEntry(tab)
        self.epsku_entry.grid(row=6, column=1, padx=10, pady=10, sticky="we")

        ctk.CTkLabel(tab, text="Retail Price:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.epn_rprice = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.epn_rprice.grid(row=7, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Wholesale Price:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.epn_wprice = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.epn_wprice.grid(row=8, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkLabel(tab, text="Market Price:").grid(row=9, column=0, padx=10, pady=10, sticky="w")
        self.epn_mprice = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.epn_mprice.grid(row=9, column=1, padx=10, pady=10, sticky="we")

        ctk.CTkLabel(tab, text="MRP:").grid(row=10, column=0, padx=10, pady=10, sticky="w")
        self.epn_mrp = ctk.CTkEntry(tab, placeholder_text="0.0")
        self.epn_mrp.grid(row=10, column=1, padx=10, pady=10, sticky="we")
        
        self.update_prod_btn = ctk.CTkButton(tab, text="Update Product", command=self.update_product)
        self.update_prod_btn.grid(row=11, column=0, columnspan=2, pady=20)

    def on_edit_product_select(self, choice):
        if not hasattr(self, 'all_products') or "No products" in choice:
            return
        try:
            pid = int(choice.split(" - ")[0])
            prod = next((p for p in self.all_products if p['id'] == pid), None)
            if prod:
                snap = DataEngine.get_latest_snapshot(pid)
                self.epn_entry.delete(0, 'end'); self.epn_entry.insert(0, str(prod.get('name', '')))
                self.epb_entry.delete(0, 'end'); self.epb_entry.insert(0, str(prod.get('brand', '')))
                self.eps_entry.delete(0, 'end'); self.eps_entry.insert(0, str(prod.get('pack_size', '')))
                self.epu_entry.delete(0, 'end'); self.epu_entry.insert(0, str(prod.get('units', '1.0')))
                self.eppt_entry.delete(0, 'end'); self.eppt_entry.insert(0, str(prod.get('packaging', '')))
                self.epsku_entry.delete(0, 'end'); self.epsku_entry.insert(0, str(prod.get('sku', '')))
                
                self.epn_rprice.delete(0, 'end'); self.epn_rprice.insert(0, str(snap.get('current_price', '0.0')))
                self.epn_wprice.delete(0, 'end'); self.epn_wprice.insert(0, str(snap.get('wholesale_price', '0.0')))
                self.epn_mprice.delete(0, 'end'); self.epn_mprice.insert(0, str(snap.get('market_price', '0.0')))
                self.epn_mrp.delete(0, 'end'); self.epn_mrp.insert(0, str(snap.get('mrp', '0.0')))
        except Exception:
            pass

    def save_price(self):
        prod_val = self.product_var.get()
        if "No products" in prod_val or not prod_val:
            messagebox.showerror("Error", "Select a valid product.")
            return
            
        pid = int(prod_val.split(" - ")[0])
        dt = self.date_entry.get().strip()
        
        try:
            price = float(self.price_entry.get() or 0)
            wprice = float(self.wprice_entry.get() or 0)
            mprice = float(self.mprice_entry.get() or 0)
            mrp = float(self.mrp_entry.get() or 0)
            qty = float(self.qty_entry.get() or 1.0)
            
            DataEngine.add_price_entry(pid, dt, price, wprice, mprice, mrp, qty, source="Manual Entry")
            messagebox.showinfo("Success", "Price entry added successfully!")
            
            self.price_entry.delete(0, 'end')
            self.wprice_entry.delete(0, 'end')
            self.mprice_entry.delete(0, 'end')
            self.mrp_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Error", "Price, MRP, and Quantity must be valid numbers.")
            
    def save_product(self):
        name = self.pn_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Product Name is required.")
            return
            
        brand = self.pb_entry.get().strip()
        pack = self.ps_entry.get().strip()
        try:
            units = float(self.pu_entry.get() or 1.0)
        except:
            units = 1.0
        pkg = self.ppt_entry.get().strip()
        sku = self.psku_entry.get().strip()
        
        try:
            rprice = float(self.pn_rprice.get() or 0.0)
            wprice = float(self.pn_wprice.get() or 0.0)
            mprice = float(self.pn_mprice.get() or 0.0)
            mrp = float(self.pn_mrp.get() or 0.0)
        except:
            rprice, wprice, mprice, mrp = 0.0, 0.0, 0.0, 0.0
            
        pid = DataEngine.add_new_product(name, brand, pack, units, pkg, sku)
        if pid:
            DataEngine.add_price_entry(pid, datetime.now().strftime("%Y-%m-%d"), rprice, wprice, mprice, mrp, 1.0, "Product Creation")
        
        messagebox.showinfo("Success", f"Product '{name}' created successfully!")
        
        self.pn_entry.delete(0, 'end')
        self.pb_entry.delete(0, 'end')
        self.ps_entry.delete(0, 'end')
        self.ppt_entry.delete(0, 'end')
        self.psku_entry.delete(0, 'end')
        self.pn_rprice.delete(0, 'end')
        self.pn_wprice.delete(0, 'end')
        self.pn_mprice.delete(0, 'end')
        self.pn_mrp.delete(0, 'end')
        
        self.load_products()
        self.tabview.set("Update Price Entry")

    def update_product(self):
        choice = self.edit_product_var.get()
        if not choice or "No products" in choice:
            return
            
        pid = int(choice.split(" - ")[0])
        name = self.epn_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Product Name is required.")
            return
            
        brand = self.epb_entry.get().strip()
        pack = self.eps_entry.get().strip()
        try:
            units = float(self.epu_entry.get() or 1.0)
        except:
            units = 1.0
        pkg = self.eppt_entry.get().strip()
        sku = self.epsku_entry.get().strip()
        
        DataEngine.update_product(pid, name, brand, pack, units, pkg, sku)
        
        try:
            rprice = float(self.epn_rprice.get() or 0.0)
            wprice = float(self.epn_wprice.get() or 0.0)
            mprice = float(self.epn_mprice.get() or 0.0)
            mrp = float(self.epn_mrp.get() or 0.0)
            
            # Compare to latest snapshot to avoid duplicate sequential rows, simply push daily update
            snap = DataEngine.get_latest_snapshot(pid)
            if float(snap.get('current_price', 0)) != rprice or float(snap.get('wholesale_price', 0)) != wprice or float(snap.get('market_price', 0)) != mprice or float(snap.get('mrp', 0)) != mrp:
                 DataEngine.add_price_entry(pid, datetime.now().strftime("%Y-%m-%d"), rprice, wprice, mprice, mrp, float(snap.get('quantity', 1.0)), "Product Edit")
        except Exception:
            pass
            
        messagebox.showinfo("Success", f"Product '{name}' updated successfully!")
        self.load_products()
