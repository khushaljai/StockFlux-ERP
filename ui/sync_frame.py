# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from importer import import_csv
from exporter import export_to_excel

class SyncFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Data Management", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

        self.desc_label = ctk.CTkLabel(self, text="Select a CSV or Excel file to update your product and pricing data.")
        self.desc_label.grid(row=1, column=0, pady=10)

        self.source_var = ctk.StringVar(value="Edible Oil Tracker")
        self.source_dropdown = ctk.CTkOptionMenu(self, variable=self.source_var, values=["Edible Oil Tracker", "Busy", "Stocky", "Other Format"])
        self.source_dropdown.grid(row=2, column=0, pady=10)

        self.import_button = ctk.CTkButton(self, text="Select File (CSV/Excel)", command=self.select_file, height=40)
        self.import_button.grid(row=3, column=0, pady=(20, 10))

        self.export_button = ctk.CTkButton(self, text="Export Database to Excel", command=self.export_data, height=40, fg_color="#107C41", hover_color="#185c37")
        self.export_button.grid(row=4, column=0, pady=(10, 10))
        
        self.template_button = ctk.CTkButton(self, text="Download Blank Excel Template", command=self.download_template, height=30, fg_color="transparent", border_width=1, border_color="#555555", text_color="#A0A0A0")
        self.template_button.grid(row=5, column=0, pady=(0, 20))
        
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=7, column=0, pady=10)

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=(("Excel or CSV files", "*.csv;*.xlsx;*.xls"), ("All files", "*.*"))
        )
        if filepath:
            self.start_import(filepath)

    def start_import(self, filepath):
        self.import_button.configure(state="disabled")
        self.export_button.configure(state="disabled")
        self.template_button.configure(state="disabled")
        self.progress_bar.grid(row=6, column=0, pady=10)
        self.progress_bar.start()
        self.status_label.configure(text=f"Importing {filepath}...", text_color="gray")
        
        # Run import in background
        threading.Thread(target=self.run_import, args=(filepath,), daemon=True).start()
        
    def run_import(self, filepath):
        source = self.source_var.get()
        result = import_csv(filepath, source)
        
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.import_button.configure(state="normal")
        self.export_button.configure(state="normal")
        self.template_button.configure(state="normal")
        
        if result["status"] == "success":
            msg = f"Successfully imported data.\nAdded {result['added_products']} new products\nAdded {result['added_entries']} price entries."
            self.status_label.configure(text=msg, text_color="green")
            messagebox.showinfo("Success", msg)
        else:
            msg = f"Error: {result['message']}"
            self.status_label.configure(text=msg, text_color="red")
            messagebox.showerror("Import Error", msg)

    def export_data(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if filepath:
            self.export_button.configure(state="disabled")
            self.import_button.configure(state="disabled")
            self.template_button.configure(state="disabled")
            self.progress_bar.grid(row=6, column=0, pady=10)
            self.progress_bar.start()
            self.status_label.configure(text=f"Exporting to {filepath}...", text_color="gray")
            threading.Thread(target=self.run_export, args=(filepath,), daemon=True).start()

    def run_export(self, filepath):
        result = export_to_excel(filepath)
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.export_button.configure(state="normal")
        self.import_button.configure(state="normal")
        self.template_button.configure(state="normal")
        
        if result["status"] == "success":
            self.status_label.configure(text=result["message"], text_color="green")
            messagebox.showinfo("Success", result["message"])
        else:
            self.status_label.configure(text=f"Export Error: {result['message']}", text_color="red")
            messagebox.showerror("Export Error", result['message'])

    def download_template(self):
        filepath = filedialog.asksaveasfilename(
            title="Save Import Template File",
            defaultextension=".xlsx",
            initialfile="Import_Template.xlsx",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if filepath:
            try:
                import pandas as pd
                columns = [
                    "Product Name", "Brand", "Pack Size", "Units", "Pkg Type", "SKU",
                    "Date", "Retail Price", "Wholesale Price", "Market Price", "MRP", "Quantity", "Source"
                ]
                df = pd.DataFrame(columns=columns)
                df.to_excel(filepath, index=False)
                messagebox.showinfo("Success", f"Blank template saved successfully to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create template: {str(e)}")
