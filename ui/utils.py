# Copyright (c) 2026 Khushal Jain
# Licensed under the MIT License

import customtkinter as ctk

def animate_number(label_widget: ctk.CTkLabel, start_val: float, end_val: float, steps: int = 20, duration_ms: int = 500, prefix: str = "", suffix: str = "", is_float: bool = True):
    """
    Smoothly counts up/down the number displayed on a CTkLabel with an ease-out effect.
    """
    if not label_widget.winfo_exists():
        return
        
    step_duration = max(10, duration_ms // steps)
    
    def step_func(current_step):
        if not label_widget.winfo_exists():
            return
            
        if current_step >= steps:
            if is_float:
                # Add commas for thousands
                final_str = f"{prefix}{end_val:,.2f}{suffix}"
            else:
                final_str = f"{prefix}{int(end_val)}{suffix}"
            label_widget.configure(text=final_str)
            return
            
        progress = current_step / steps
        # ease-out cubic
        eased_progress = 1 - pow(1 - progress, 3)
        current_val = start_val + (end_val - start_val) * eased_progress
        
        if is_float:
            val_str = f"{prefix}{current_val:,.2f}{suffix}"
        else:
            val_str = f"{prefix}{int(current_val)}{suffix}"
            
        label_widget.configure(text=val_str)
        label_widget.after(step_duration, step_func, current_step + 1)
        
    step_func(0)

def enhance_card(frame: ctk.CTkFrame):
    """
    Applies an attractive but minimalist styling to cards.
    """
    frame.configure(
        fg_color="#1E1E1E",
        corner_radius=15,
        border_width=1,
        border_color="#333333"
    )
