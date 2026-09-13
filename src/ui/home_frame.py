"""
home_frame.py
"""

import customtkinter as ctk
from src.modal import AddItemModal
from src.database import get_all_items, delete_item, edit_item


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

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
            row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row.grid(row=i * 2, column=0, sticky="ew", padx=8, pady=(8, 0))
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row, text=name, font=ctk.CTkFont(size=14, weight="bold")
            ).grid(row=0, column=0, sticky="w")

            ctk.CTkLabel(
                row, text=f"📍 {location}", text_color="gray", font=ctk.CTkFont(size=12)
            ).grid(row=1, column=0, sticky="w")

            ctk.CTkButton(
                row, text="🗑", width=26, height=26, corner_radius=13,
                fg_color="#e74c3c", hover_color="#c0392b",
                font=ctk.CTkFont(size=12),
                border_spacing=0,
                command=lambda i=item_id: self.handle_delete(i),
            ).grid(row=0, column=1, rowspan=2, sticky="e")

            ctk.CTkButton(
                row, text="✏", width=26, height=26, corner_radius=13,
                fg_color="#e7e43c", hover_color="#c0b12b",
                font=ctk.CTkFont(size=12),
                text_color="#000",
                border_spacing=0,
                command=lambda i=item_id: self.handle_edit(i),
            ).grid(row=0, column=2, rowspan=2, sticky="e")

            if i < len(items) - 1:
                divider = ctk.CTkFrame(
                    self.list_frame,
                    height=2,
                    corner_radius=0,
                    border_width=0,
                    fg_color="gray30",
                )
                divider.grid(row=i * 2 + 1, column=0, sticky="ew", padx=8, pady=8)

    def handle_delete(self, item_id: int):
        delete_item(item_id, self.user_id)
        self.refresh_items()

    def handle_edit(self, item_id: int):
        edit_item(item_id, self.user_id)
        self.refresh_items()