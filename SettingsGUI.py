"""
SettingsGUI.py
Settings menu for changing options found in Settings.py
Last Edited: 11/8/2024
"""

import customtkinter as ctk
import tkinter as tk

class SettingsGUI:
    """
    This class contains the GUI for the Settings menu
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create a main frame for the settings page
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Creating fonts
        headerfont = ctk.CTkFont(family="Garet", size=100)
        buttonfont = ctk.CTkFont(family="Garet", size=28, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")

        # button functions
        def back_function():
            self.controller.show_menu_gui()

        # Welcome label
        self.welcome_label = ctk.CTkLabel(master=self.frame, text="Settings", font=headerfont, text_color="black")
        self.welcome_label.place(relx=0.5, rely=0.18, anchor=tk.CENTER)

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20  # from Choice GUI
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        #known threshold slider

    def destroy(self):
        self.frame.destroy()
