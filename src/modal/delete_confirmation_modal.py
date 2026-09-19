'''
delete_confirmation_modal.py
'''

import customtkinter as ctk
from src.database import delete_item

class DelConfirmModal(ctk.CTkToplevel):
    def __init__(self, master, item_id, user_id, on_confirm=None):
        super().__init__(master)
        self.on_confirm = on_confirm
        self.item_id = item_id
        self.user_id = user_id

        self.title("Delete Item")
        self.geometry("260x180")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self, text="Are you sure you want to delete this item?",
            font=ctk.CTkFont(size=15, weight="bold"),
            wraplength=220,
        ).grid(row=0, column=0, columnspan=2, pady=(24, 16), padx=16)

        ctk.CTkButton(
            self, text="Yes", width=90, height=40,
            fg_color="#e74c3c", hover_color="#c0392b",
            command=self.handle_confirm,
        ).grid(row=1, column=0, padx=(16, 8), pady=(0, 16))

        ctk.CTkButton(
            self, text="No", width=90, height=40,
            fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"),
            command=self.destroy,
        ).grid(row=1, column=1, padx=(8, 16), pady=(0, 16))

    def handle_confirm(self):
        self.destroy()
        delete_item(item_id=self.item_id, user_id=self.user_id)
        if self.on_confirm:
            self.master.after(10, self.on_confirm)