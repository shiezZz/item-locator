"""
verify_frame.py
Screen where the user enters the code emailed to them.
"""

import customtkinter as ctk
from src.db import verify_code, resend_code
from src.utils import send_verification_email


class VerifyFrame(ctk.CTkFrame):
    def __init__(self, master, app, username):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.username = username

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self, corner_radius=16, width=360, height=300)
        card.grid(row=0, column=0)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="Check your email", font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(40, 8))

        ctk.CTkLabel(
            card, text="Enter the 6-digit code we sent you", font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, pady=(0, 16))

        self.code_entry = ctk.CTkEntry(
            card, placeholder_text="Code", width=260, height=40, corner_radius=10
        )
        self.code_entry.grid(row=2, column=0, pady=8)
        self.code_entry.bind("<Return>", lambda e: self.handle_verify())

        self.error_label = ctk.CTkLabel(
            card, text="", text_color="#e74c3c", font=ctk.CTkFont(size=12)
        )
        self.error_label.grid(row=3, column=0, pady=(4, 0))

        ctk.CTkButton(
            card, text="Verify", width=260, height=40, corner_radius=10,
            command=self.handle_verify,
        ).grid(row=4, column=0, pady=(16, 8))

        resend_link = ctk.CTkLabel(
            card, text="Resend code", text_color="#3b8ed0", cursor="hand2",
            font=ctk.CTkFont(size=12, underline=True),
        )
        resend_link.grid(row=5, column=0, pady=(4, 0))
        resend_link.bind("<Button-1>", lambda e: self.handle_resend())

    def _show(self, message: str, ok: bool = False):
        self.error_label.configure(
            text=message, text_color="#2ecc71" if ok else "#e74c3c"
        )

    def handle_verify(self):
        code = self.code_entry.get().strip()
        result = verify_code(self.username, code)

        if result == "ok":
            self.after(10, self.app.show_login)
        elif result == "expired":
            self._show("This code has expired. Click 'Resend code'.")
        else:
            self._show("Invalid code.")

    def handle_resend(self):
        result = resend_code(self.username)
        if result is None:
            self._show("Couldn't resend the code.")
            return

        email, code = result
        send_verification_email(email, code)
        self._show("A new code was sent to your email.", ok=True)