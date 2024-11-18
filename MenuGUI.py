"""
MenuGUI.py
================
This is the GUI for the main menu screen.
After successful login or registration,
the user is taken to this screen. They can
choose from the following options:

    1. Exit the application
    2. Multiple choice flashcards
    3. Text-based flashcards
    4. Review mode
    5. Statistics
    6. Settings
    7. About

Version: 4.0
Since: 11-11-2024
"""

import customtkinter as ctk
import tkinter as tk
import Settings as Settings
import pygame
import logging
from PIL import Image

class MenuGUI:
    def __init__(self, controller):
        """
        Initialize the main menu GUI screen with buttons for each option.
        """
        self.controller = controller
        self.app = controller.app

        # Configure the main frame of the window
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Define fonts for different components
        buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")  # Font for buttons
        titlefont = ctk.CTkFont(family="Garet", size=75, weight="bold", slant="italic")  # Font for title

        # Define icons for each button
        choice_icon = ctk.CTkImage(light_image=Image.open("Assets/choice-icon.png"), size=(40, 40))
        text_icon = ctk.CTkImage(light_image=Image.open("Assets/text-icon.png"), size=(40, 40))
        review_icon = ctk.CTkImage(light_image=Image.open("Assets/review-icon.png"), size=(40, 40))
        settings_icon = ctk.CTkImage(light_image=Image.open("Assets/settings-icon.png"), size=(40, 40))
        stats_icon = ctk.CTkImage(light_image=Image.open("Assets/stats-icon.png"), size=(40, 40))
        exit_icon = ctk.CTkImage(light_image=Image.open("Assets/exit-icon.png"), size=(40, 40))
        about_icon = ctk.CTkImage(light_image=Image.open("Assets/about-icon.png"), size=(40, 40))

        # Define button functions for different actions
        def choice_function():
            """Show the Multiple Choice Flashcards GUI."""
            self.controller.show_choice_gui()

        def text_function():
            """Show the Text-Input Flashcards GUI."""
            self.controller.show_text_gui()

        def review_function():
            """Show the Review Mode GUI."""
            self.controller.show_review_gui()

        def settings_function():
            """Show the Settings GUI."""
            self.controller.show_settings_gui()

        def stats_function():
            """Show the Statistics GUI."""
            self.controller.show_stats_gui()

        def about_function():
            """Show the About page GUI."""
            self.controller.show_about_gui()

        def exit_button():
            """Exit the application, save data, and close the app."""
            print("Exiting application")
            self.controller.study_window.word_dict_to_csv(f"{Settings.username}_{Settings.LANGUAGE}.csv")
            logging.info("Exiting application.")
            pygame.quit()
            self.app.destroy()

        # Title label "Time to get SMRT!"
        self.title_label = ctk.CTkLabel(master=self.frame, text="Time to get SMRT!", text_color="black", font=titlefont)
        self.title_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)  # Positioning title in the center

        # Define button parameters: colors, texts, functions, and icons
        button_colors = ["#f37d59", "#0f606b", "#b69352","#ffc24a", "#aeb883"]
        button_texts = ["Multiple Choice Flashcards", "Text-Input Flashcards", "Review Mode", "Statistics", "Settings"]
        button_commands = [choice_function, text_function, review_function, stats_function, settings_function]
        button_icons = [choice_icon, text_icon, review_icon, stats_icon, settings_icon]

        # Create and position the buttons for each option on the menu
        for i in range(5):
            button = ctk.CTkButton(
                master=self.frame, text=button_texts[i], font=buttonfont,
                fg_color=button_colors[i], text_color="#ffffff",  # White text color
                width=900, height=80, command=button_commands[i], corner_radius=15,
                image=button_icons[i], compound="left"  # Button with icon and text
            )
            button.place(relx=0.5, rely=0.3 + (i * 0.125), anchor=tk.CENTER)  # Vertical spacing between buttons

        # About button at the bottom-right of the screen
        about_btn = ctk.CTkButton(
            master=self.frame, text="About", font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=150, height=60, fg_color="#e38368", text_color="white",
            command=about_function, corner_radius=15,
            image=about_icon, compound="left"
        )
        about_btn.place(relx=0.90, rely=0.95, anchor=tk.CENTER)  # Positioned at bottom-right

        # Exit button at the bottom-center of the screen
        exit_btn = ctk.CTkButton(
            master=self.frame, text="EXIT", font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=120, height=60, fg_color="#d9534f", text_color="white",
            command=exit_button, corner_radius=15,
            image=exit_icon, compound="left"
        )
        exit_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  # Positioned at bottom-center

    def destroy(self):
        """Destroy the frame and all its components when the GUI is closed."""
        self.frame.destroy()
