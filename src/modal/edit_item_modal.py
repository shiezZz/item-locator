'''
edit_item_modal.py
'''

import customtkinter as ctk
from tkinter import filedialog
from src.database import edit_item, get_item, IMAGES_DIR
import shutil
import os





class EditItemModal(ctk.CTkToplevel):
    def __init__(self, master, user_id, item_id, on_success=None):
        super().__init__(master)
        self.user_id = user_id
        self.on_success = on_success
        self.item_id = item_id
        self.selected_image_path = None
        name, location, category, notes, date_updated, image_path = get_item(item_id=self.item_id, user_id=self.user_id)
        r = 0

        self.image_label = ctk.CTkLabel(self, text="No image selected", text_color="gray")
        self.image_label.grid(row=r, column=0, pady=4)
        r+=1

        ctk.CTkButton(
            self, text="Choose Image", width=280, height=36,
            command=self.choose_image,
        ).grid(row=r, column=0, pady=(0, 8))
        r+=1

        self.title("Edit Item")
        self.geometry("360x450")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="EDIT ITEM", font=ctk.CTkFont(size=18, weight="bold")).grid(row=r,column=0, pady=(24, 16))
        r+=1

        self.name_entry = ctk.CTkEntry(self, width=280, height=40, )
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=r, column=0, pady=8)
        r+=1

        self.location_entry = ctk.CTkEntry(self, width=280, height=40)
        self.location_entry.insert(0, location)
        self.location_entry.grid(row=r, column=0,pady=8)
        r+=1

        self.category_entry = ctk.CTkEntry(self, width=280, height=40)
        self.category_entry.insert(0, category)
        self.category_entry.grid(row=r, column=0,pady=8)
        r+=1

        self.notes_entry = ctk.CTkEntry(self, width=280, height=40)
        self.notes_entry.insert(0, notes)
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

    def handle_save(self):
        name= self.name_entry.get().strip()
        location= self.location_entry.get().strip()
        category= self.category_entry.get().strip()
        notes= self.notes_entry.get().strip()

        if not name or not location:
            self.error_label.configure(text="Name and location are required.")
            return

        edit_item(user_id=self.user_id, item_id=self.item_id, name=name, location=location, category=category, notes=notes)

        if self.on_success:
            self.on_success()

        self.destroy()

    def _center_over(self, master):
        master.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - 180
        y = master.winfo_y() + (master.winfo_height() // 2) - 210
        self.geometry(f"+{x}+{y}")

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")]
        )
        if path:
            self.selected_image_path = path
            self.image_label.configure(text=os.path.basename(path))
