"""
login_frame.py
The login screen. Calls app.show_home() on successful login.
"""

import customtkinter as ctk
from database import verify_user


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        # Center everything in the middle of the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self, corner_radius=16, width=360, height=420)
        card.grid(row=0, column=0)
        card.grid_propagate(False)

        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="📍", font=ctk.CTkFont(size=40)
        ).grid(row=0, column=0, pady=(40, 0))

        ctk.CTkLabel(
            card, text="RE:Item", font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=1, column=0, pady=(8, 24))

        self.username_entry = ctk.CTkEntry(
            card, placeholder_text="Username", width=260, height=40, corner_radius=10
        )
        self.username_entry.grid(row=2, column=0, pady=8)

        self.password_entry = ctk.CTkEntry(
            card,
            placeholder_text="Password",
            show="•",
            width=260,
            height=40,
            corner_radius=10,
        )
        self.password_entry.grid(row=3, column=0, pady=8)
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

        self.error_label = ctk.CTkLabel(
            card, text="", text_color="#e74c3c", font=ctk.CTkFont(size=12)
        )
        self.error_label.grid(row=4, column=0, pady=(4, 0))

        ctk.CTkButton(
            card,
            text="Log In",
            width=260,
            height=40,
            corner_radius=10,
            command=self.handle_login,
        ).grid(row=5, column=0, pady=(16, 8))

        link_label = ctk.CTkLabel(
            card,
            text="Don't have an account? Sign up",
            text_color="#3b8ed0",      
            cursor="hand2",             
            font=ctk.CTkFont(size=12, underline=True),
        )
        link_label.grid(row=7, column=0, pady=(12, 0))

        link_label.bind("<Button-1>", lambda e: self.after(10, self.app.show_signup))

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Please enter both fields.")
            return

        result, user_id = verify_user(username, password)
        if result == "ok":
            self.error_label.configure(text="")
            self.app.show_home(username, user_id)
        elif result == "unverified":
            self.error_label.configure(text="Please verify your email first.")
        else:
            self.error_label.configure(text="Invalid username or password.")