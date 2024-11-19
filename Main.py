"""
Main.py
================
This is the headquarters for the
SMRT Vocab application. Main allows
the program to be executed.

Version: 3.0
Since: 11-17-2024
"""

import customtkinter as ctk

#import Settings
from LoginGUI import LoginGUI
#from WalkingWindow import WalkingWindow
from MenuGUI import MenuGUI
from ChoiceGUI import ChoiceGUI
from TextGUI import TextGUI
from SettingsGUI import SettingsGUI
from StatsGUI import StatsGUI
from AboutGUI import AboutGUI
from ReviewGUI import ReviewGUI
import Settings
import pygame
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

        #init pygame for TTS
        pygame.mixer.init()

        # Initialize the main application window
        self.app = ctk.CTk()
        self.app.iconbitmap("Assets/SMRT_Vocab_logo.ico")
        self.app.geometry("1000x1000")
        self.app._state_before_windows_set_titlebar_color = 'zoomed'
        self.app.title("SMRT")
        self.study_window = None

        # Sets default color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Initialize shared resources

        self.current_frame = None

        self.show_login_gui()

        # Start the main event loop
        self.app.mainloop()

    # LoginGUI
    def show_login_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginGUI(self)

    # MenuGUI
    def show_menu_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MenuGUI(self)

    # ChoiceGUI
    def show_choice_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ChoiceGUI(self)

    # TextGUI
    def show_text_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TextGUI(self)

    #ReviewGUI
    def show_review_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ReviewGUI(self)

    # SettingsGUI
    def show_settings_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SettingsGUI(self)

    # StatsGUI
    def show_stats_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = StatsGUI(self)

    # AboutGUI
    def show_about_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AboutGUI(self)

    # Closing the application
    def save_and_close(self):
        """Save user data and clean up program before exiting"""
        csv_name = f"{Settings.username}_{Settings.LANGUAGE}.csv"
        self.study_window.word_dict_to_csv(csv_name)
        pygame.quit()
        if self.current_frame:
            self.current_frame.destroy()
        self.app.destroy()

if __name__ == "__main__":
    GUI()
