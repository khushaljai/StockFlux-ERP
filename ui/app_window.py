# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk
from .dashboard_frame import DashboardFrame
from .sync_frame import SyncFrame
from .add_entry_frame import AddEntryFrame
from .inventory_frame import InventoryFrame
from database import init_db
from data_engine import DataEngine

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Init DB
        init_db()

        self.title("Price Tracking & Analytics")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Business Analytics", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.dashboard_button = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.inventory_button = ctk.CTkButton(self.sidebar_frame, text="Inventory & Catalog", command=self.show_inventory)
        self.inventory_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.add_entry_button = ctk.CTkButton(self.sidebar_frame, text="Add Entry", command=self.show_add_entry)
        self.add_entry_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.sync_button = ctk.CTkButton(self.sidebar_frame, text="Data Management", command=self.show_sync)
        self.sync_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set("Dark")

        # create frames
        self.dashboard_frame = DashboardFrame(self)
        self.inventory_frame = InventoryFrame(self)
        self.add_entry_frame = AddEntryFrame(self)
        self.sync_frame = SyncFrame(self)
        
        # Start with Dashboard
        self.show_dashboard()

    def show_dashboard(self):
        self.sync_frame.grid_forget()
        self.add_entry_frame.grid_forget()
        self.inventory_frame.grid_forget()
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.dashboard_frame.refresh_data()

    def show_inventory(self):
        self.dashboard_frame.grid_forget()
        self.sync_frame.grid_forget()
        self.add_entry_frame.grid_forget()
        self.inventory_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.inventory_frame.refresh_data()

    def show_add_entry(self):
        self.dashboard_frame.grid_forget()
        self.sync_frame.grid_forget()
        self.inventory_frame.grid_forget()
        self.add_entry_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.add_entry_frame.load_products()

    def show_sync(self):
        self.dashboard_frame.grid_forget()
        self.add_entry_frame.grid_forget()
        self.inventory_frame.grid_forget()
        self.sync_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
