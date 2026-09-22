"""
main.py
Entry point. Run this file to start the app: python main.py
"""

import customtkinter as ctk
from src.database import init_db, migrate_add_date_updated
from src.ui import LoginFrame, HomeFrame, SignUpFrame, VerifyFrame

ctk.set_appearance_mode("dark")       # "dark", "light", or "system"
ctk.set_default_color_theme("blue")   # "blue", "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Item Locator")
        self.geometry("480x720")
        self.minsize(400, 640)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_frame = None
        self.show_login()

    def show_login(self):
        login = LoginFrame(self,self)  
        self._switch_frame(login)

    def show_home(self, username: str, user_id: int):
        home = HomeFrame(self, self)
        home.set_username(username, user_id)
        self._switch_frame(home)

    def show_signup(self):
        signup = SignUpFrame(self,self)
        self._switch_frame(signup)

    def show_verify(self, username: str):
        verify = VerifyFrame(self, self, username)
        self._switch_frame(verify)

    def _switch_frame(self, new_frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")



if __name__ == "__main__":
    init_db()
    migrate_add_date_updated()
    app = App()
    app.mainloop()
