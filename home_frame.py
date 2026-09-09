"""
home_frame.py
"""

import customtkinter as ctk
from add_item_modal import AddItemModal
from database import get_all_items


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Top bar: greeting + logout ---
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 8))
        top_bar.grid_columnconfigure(0, weight=1)

        self.greeting_label = ctk.CTkLabel(
            top_bar, text="Hi there 👋", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.greeting_label.grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            top_bar,
            text="Log Out",
            width=90,
            height=32,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.app.show_login,
        ).grid(row=0, column=1, sticky="e")

        search_bar = ctk.CTkFrame(self, fg_color="transparent")
        search_bar.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        search_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search for an item...",
            height=40,
            corner_radius=10,
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            search_bar,
            text="+ Add Item",
            height=40,
            corner_radius=10,
            command=self.add_item_placeholder,
        ).grid(row=0, column=1)

        # --- Scrollable item list area (placeholder) ---
        self.list_frame = ctk.CTkScrollableFrame(
            self, corner_radius=12, label_text="Your Items"
        )
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(8, 24))
        self.list_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.list_frame,
            text="No items yet — this is where your item cards will show up.",
            text_color="gray",
        ).grid(row=0, column=0, pady=20)

    def set_username(self, username: str, user_id: int):
        self.user_id = user_id
        self.greeting_label.configure(text=f"Hi, {username} 👋")
        self.refresh_items()

    def add_item_placeholder(self):
        AddItemModal(self.app, user_id=self.user_id, on_success=self.refresh_items)

    def refresh_items(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        items = get_all_items(self.user_id) 

        if not items:
            ctk.CTkLabel(
                self.list_frame, text="No items yet.", text_color="gray"
            ).grid(row=0, column=0, pady=20)
            return

        for i, (item_id, name, location, category, notes) in enumerate(items):
            row = ctk.CTkFrame(self.list_frame, corner_radius=10)
            row.grid(row=i, column=0, sticky="ew", pady=4, padx=4)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row, text=name, font=ctk.CTkFont(size=14, weight="bold")
            ).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))

            ctk.CTkLabel(
                row, text=f"📍 {location}", text_color="gray"
            ).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))