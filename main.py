# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk
from ui.app_window import AppWindow

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
