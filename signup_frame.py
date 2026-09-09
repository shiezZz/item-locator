"""
signup_frame.py
The signup screen. 
"""

import customtkinter as ctk
from database import create_account
from email_utils import send_verification_email


class SignUpFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        # Center everything in the middle of the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self, corner_radius=16, width=360, height=620)
        card.grid(row=0, column=0)
        card.grid_propagate(False)

        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="📍", font=ctk.CTkFont(size=32)
        ).grid(row=0, column=0, pady=(24, 0))

        ctk.CTkLabel(
            card, text="RE:Item", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=1, column=0, pady=(4, 4))

        ctk.CTkLabel(
                    card, text="Create Account", font=ctk.CTkFont(size=14)
                ).grid(row=2, column=0, pady=(0, 16))

        self.email_sign = ctk.CTkEntry(
            card, placeholder_text="Email", width=260, height=40, corner_radius=10
        )
        self.email_sign.grid(row=3, column=0, pady=6)

        self.username_sign = ctk.CTkEntry(
            card, placeholder_text="Username", width=260, height=40, corner_radius=10
        )
        self.username_sign.grid(row=4, column=0, pady=6)

        self.password_sign = ctk.CTkEntry(
            card,
            placeholder_text="Password",
            show="•",
            width=260,
            height=40,
            corner_radius=10,
        )
        self.password_sign.grid(row=5, column=0, pady=6)

        self.confirm_password_sign = ctk.CTkEntry(
            card,
            placeholder_text="Confirm Password",
            show="•",
            width=260,
            height=40,
            corner_radius=10,
        )

        self.confirm_password_sign.grid(row=6, column=0, pady=6)
        self.confirm_password_sign.bind("<Return>", lambda e: self.handle_signup())

        self.error_label = ctk.CTkLabel(
            card, text="", text_color="#e74c3c", font=ctk.CTkFont(size=12)
        )
        self.error_label.grid(row=7, column=0, pady=(2, 0))

        ctk.CTkButton(
            card,
            text="Create an Account",
            width=260,
            height=40,
            corner_radius=10,
            command=self.handle_signup,
        ).grid(row=8, column=0, pady=(14, 6))

        link_label = ctk.CTkLabel(
            card,
            text="Already have an account? Sign in",
            text_color="#3b8ed0",      
            cursor="hand2",             
            font=ctk.CTkFont(size=12, underline=True),
        )
        link_label.grid(row=9, column=0, pady=(8, 16))
        
        link_label.bind("<Button-1>", lambda e: self.after(10, self.app.show_login))

    def handle_signup(self):
        username = self.username_sign.get().strip()
        email = self.email_sign.get().strip()
        password = self.password_sign.get().strip()
        confirm_password = self.confirm_password_sign.get().strip()

        if not username or not email or not password or not confirm_password:
            self.error_label.configure(text="Please fill all of the fields.")
            return

        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match.")
            return

        code = create_account(username, email, password)
        if code is None:
            self.error_label.configure(text="Username or email already taken.")
            return

        send_verification_email(email, code)
        self.error_label.configure(text="")
        self.after(10, lambda: self.app.show_verify(username))
