# main.py

import customtkinter as ctk

import Settings
from LoginGUI import LoginGUI
from WalkingWindow import WalkingWindow
from MenuGUI import MenuGUI
from ChoiceGUI import ChoiceGUI
from TextGUI import TextGUI
from SettingsGUI import SettingsGUI

import logging

"""
set up logging configuration
to use: 
import logging
logging.info(message)
"""
logging.basicConfig(
    filename="smrt.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GUI:
    def __init__(self):
        # Mark log with new execution
        logging.info("SMRT Vocab app started")

        # Initialize the main application window
        self.app = ctk.CTk()
        self.app.geometry("1000x1000")
        self.app._state_before_windows_set_titlebar_color = 'zoomed'
        self.app.title("SMRT")

        # Sets default color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Initialize shared resources

        self.current_frame = None

        self.show_login_gui()

        # Start the main event loop
        self.app.mainloop()

    def show_login_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginGUI(self)

    def show_menu_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MenuGUI(self)

    def show_choice_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ChoiceGUI(self)
    
    def show_text_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TextGUI(self)

    def show_settings_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SettingsGUI(self)


if __name__ == "__main__":
    GUI()
