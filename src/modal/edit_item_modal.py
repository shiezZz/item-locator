'''
edit_item_modal.py
'''

import customtkinter as ctk
from src.database import edit_item

class EditItemModal(ctk.CTkToplevel):
    def __init__(self, master, user_id, item_id, on_success=None):
        super().__init__(master)
        self.user_id = user_id
        self.on_success = on_success
        self.item_id = item_id
        r = 0

        self.title("Add Item")
        self.geometry("360x450")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="ADD ITEM", font=ctk.CTkFont(size=18, weight="bold")).grid(row=r,column=0, pady=(24, 16))
        r+=1

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Item Name (e.g. Wallet)", width=280, height=40)
        self.name_entry.grid(row=r, column=0, pady=8)
        r+=1

        self.location_entry = ctk.CTkEntry(self, placeholder_text="Location (e.g. Inside 2nd Drawer)", width=280, height=40)
        self.location_entry.grid(row=r, column=0,pady=8)
        r+=1

        self.category_entry = ctk.CTkEntry(self, placeholder_text="Category (Optional)", width=280, height=40)
        self.category_entry.grid(row=r, column=0,pady=8)
        r+=1

        self.notes_entry = ctk.CTkEntry(self, placeholder_text="Notes (Optional)", width=280, height=40)
        self.notes_entry.grid(row=r, column=0,pady=8)
        r+=1

        self.error_label = ctk.CTkLabel(
            self, text="", text_color="#e74c3c", font=ctk.CTkFont(size=12)
        )
        self.error_label.grid(row=r, column=0, pady=(4, 0))
        r+=1

        ctk.CTkButton(self, text="Save Item", width=280, height=40, command=self.handle_save).grid(row=r,column=0,pady=(16,8))
        r+=1
        ctk.CTkButton(self, text="Cancel", width=280, height=40, command=self.destroy, fg_color="#e74c3c", border_width=1,text_color=("gray10", "gray90"), hover_color="#85261b").grid(row=r, column=0, pady=(0,16))

        self.after(10, lambda: self._center_over(master))        