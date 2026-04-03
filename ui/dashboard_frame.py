# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk
from tkinter import ttk
from data_engine import DataEngine
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # --- Top Bar (Selector) ---
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        ctk.CTkLabel(self.top_bar, text="Select Product:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        
        self.product_var = ctk.StringVar(value="All")
        self.product_selector = ctk.CTkOptionMenu(self.top_bar, variable=self.product_var, command=self.on_product_select)
        self.product_selector.pack(side="left", fill="x", expand=True)

        # --- Cards Section ---
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        self.cards_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        
        self.card_price = self.create_card(self.cards_frame, "Retail Price", "₹0.00", 0)
        self.card_wprice = self.create_card(self.cards_frame, "Wholesale", "₹0.00", 1)
        self.card_mprice = self.create_card(self.cards_frame, "Market Price", "₹0.00", 2)
        self.card_mrp = self.create_card(self.cards_frame, "MRP", "₹0.00", 3)
        self.card_diff = self.create_card(self.cards_frame, "B2B Margin", "₹0.00", 4)
        self.card_diff2 = self.create_card(self.cards_frame, "Retail Margin", "₹0.00", 5)
        self.card_updated = self.create_card(self.cards_frame, "Updated", "-", 6)
        
        # --- Details Section ---
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        self.details_label = ctk.CTkLabel(self.details_frame, text="Product Details", font=ctk.CTkFont(size=18, weight="bold"))
        self.details_label.pack(pady=10)
        
        self.details_text = ctk.CTkTextbox(self.details_frame, state="disabled", fg_color="transparent", font=ctk.CTkFont(size=14))
        self.details_text.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Chart Section ---
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 0))
        
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor('#2b2b2b') # dark theme match
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#2b2b2b')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- Bottom Table Section ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(20, 0))
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        columns = ("Date", "Retail", "Wholesale", "Market", "MRP", "Quantity", "Source")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # define table styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#333333", foreground="white", fieldbackground="#333333", rowheight=25)
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        self.all_products = []

    def create_card(self, parent, title, val, col):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=col, sticky="nsew", padx=8, pady=5)
        
        try:
            from .utils import enhance_card
            enhance_card(frame)
        except ImportError:
            pass
            
        lbl_title = ctk.CTkLabel(frame, text=title, text_color="#A0A0A0", font=ctk.CTkFont(size=12))
        lbl_title.pack(pady=(15, 5))
        lbl_val = ctk.CTkLabel(frame, text=val, font=ctk.CTkFont(size=26, weight="bold"), text_color="#FFFFFF")
        lbl_val.pack(pady=(0, 15))
        lbl_val._current_val = 0.0
        return lbl_val

    def refresh_data(self):
        self.all_products = DataEngine.get_all_products()
        if not self.all_products:
            self.product_selector.configure(values=["No Data Found"])
            self.product_var.set("No Data Found")
            return
            
        values = [f"{p['id']} - {p['name']} ({p['brand']})" for p in self.all_products]
        self.product_selector.configure(values=values)
        if values:
            if self.product_var.get() == "All" or self.product_var.get() not in values:
                self.product_var.set(values[0])
            self.on_product_select(self.product_var.get())

    def on_product_select(self, choice):
        if not self.all_products or "No Data" in choice: return
        
        product_id = int(choice.split(" - ")[0])
        snap = DataEngine.get_latest_snapshot(product_id)
        if snap:
            from .utils import animate_number
            price = float(snap.get('current_price', 0))
            wprice = float(snap.get('wholesale_price', 0))
            mprice = float(snap.get('market_price', 0))
            mrp = float(snap.get('mrp', 0))
            diff1 = mprice - wprice
            diff2 = mprice - price
            
            animate_number(self.card_price, getattr(self.card_price, '_current_val', 0.0), price, prefix="₹")
            self.card_price._current_val = price
            
            animate_number(self.card_wprice, getattr(self.card_wprice, '_current_val', 0.0), wprice, prefix="₹")
            self.card_wprice._current_val = wprice
            
            animate_number(self.card_mprice, getattr(self.card_mprice, '_current_val', 0.0), mprice, prefix="₹")
            self.card_mprice._current_val = mprice
            
            animate_number(self.card_mrp, getattr(self.card_mrp, '_current_val', 0.0), mrp, prefix="₹")
            self.card_mrp._current_val = mrp
            
            animate_number(self.card_diff, getattr(self.card_diff, '_current_val', 0.0), diff1, prefix="₹")
            self.card_diff._current_val = diff1

            animate_number(self.card_diff2, getattr(self.card_diff2, '_current_val', 0.0), diff2, prefix="₹")
            self.card_diff2._current_val = diff2
            
            self.card_updated.configure(text=str(snap.get('date', '-')))
            
            # Details text update
            details = f"Brand:\t\t{snap.get('brand')}\n"
            details += f"Product:\t\t{snap.get('name')}\n"
            details += f"Pack Size:\t{snap.get('pack_size')}\n"
            details += f"Units:\t\t{snap.get('units')}\n"
            details += f"Packaging:\t{snap.get('packaging')}\n"
            details += f"SKU:\t\t{snap.get('sku')}\n"
            
            self.details_text.configure(state="normal")
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", details)
            self.details_text.configure(state="disabled")
            
        history = DataEngine.get_price_history(product_id)
        self.update_table(history)
        self.update_chart(history)

    def update_table(self, history):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in history:
            self.tree.insert("", "end", values=(row['date'], f"₹{row['current_price']}", f"₹{row['wholesale_price']}", f"₹{row.get('market_price', 0.0)}", f"₹{row['mrp']}", row['quantity'], row['source']))

    def update_chart(self, history):
        self.ax.clear()
        if history:
            # reverse history for chronological charting
            hist_asc = list(reversed(history))
            dates = [h['date'] for h in hist_asc]
            prices = [h['current_price'] for h in hist_asc]
            wprices = [h.get('wholesale_price', 0.0) for h in hist_asc]
            mprices = [h.get('market_price', 0.0) for h in hist_asc]
            
            self.ax.plot(dates, prices, marker='o', color='#1f538d', linewidth=2, label='Retail Price')
            self.ax.plot(dates, wprices, marker='s', color='#107C41', linewidth=2, label='Wholesale Price')
            self.ax.plot(dates, mprices, marker='^', color='#A83232', linewidth=2, label='Market Price')
            
            self.ax.set_title("Price Trend", color="white")
            self.ax.tick_params(axis='x', rotation=45, colors='white')
            
            # Add Legend
            self.ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
            
        self.figure.tight_layout()
        self.canvas.draw()
