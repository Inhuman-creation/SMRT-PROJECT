# main.py

import customtkinter as ctk
from WalkingWindow import WalkingWindow
from MenuGUI import MenuGUI
from ChoiceGUI import ChoiceGUI


class GUI:
    def __init__(self):
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
        self.study_window.read_from_csv("Spanish.csv", num_rows=10)

        # Start with MenuGUI
        self.current_frame = None
        self.show_menu_gui()

        # Start the main event loop
        self.app.mainloop()

    def show_menu_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MenuGUI(self)

    def show_choice_gui(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ChoiceGUI(self)


if __name__ == "__main__":
    GUI()
