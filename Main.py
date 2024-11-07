# main.py

import customtkinter as ctk

from LoginGUI import LoginGUI
from WalkingWindow import WalkingWindow
from MenuGUI import MenuGUI
from ChoiceGUI import ChoiceGUI
from TextGUI import TextGUI

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
        self.study_window = WalkingWindow(size=10)
        self.study_window.read_from_csv("Template_Spanish.csv", num_rows=10) #TODO: read from user's csv

        # Start with MenuGUI ORIGINAL PLACEMENT
        #self.current_frame = None
        #self.show_menu_gui()

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


if __name__ == "__main__":
    GUI()
