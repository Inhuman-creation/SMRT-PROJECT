# =====================
# MenuGUI.py
# Latest version: Nov 11 2024
# Main menu selection screen
# =====================

import customtkinter as ctk
import tkinter as tk
import Settings as Settings
#from functools import partial

class MenuGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Configure main frame
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Fonts
        buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")  # Larger font for buttons
        titlefont = ctk.CTkFont(family="Garet", size=75, weight="bold", slant="italic")  # Font for title text

        # Button functions
        def choice_function():
            self.controller.show_choice_gui()

        def text_function():
            self.controller.show_text_gui()

        def review_function():
            self.controller.show_review_gui()

        #def placeholder_function():
        #    print("Placeholder function")

        def settings_function():
            self.controller.show_settings_gui()

        def stats_function():
            self.controller.show_stats_gui()

        def about_function():
            self.controller.show_about_gui()

        def exit_button():
            print("Exiting application")
            self.controller.study_window.word_dict_to_csv(f"{Settings.username}_{Settings.LANGUAGE}.csv")
            self.app.destroy()

        # Static title label "What would you like to do?"
        self.title_label = ctk.CTkLabel(master=self.frame, text="Time to get SMRT!", text_color="black", font=titlefont)
        self.title_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)  # Centered title

        # Create option buttons
        button_colors = ["#f37d59", "#0f606b", "#aeb883","#ffc24a", "#aeb883"]
        button_texts = ["Multiple Choice Flashcards", "Text-Input Flashcards", "Review Mode", "Statistics", "Settings"]
        button_commands = [choice_function, text_function, review_function, stats_function, settings_function]

        # Option buttons
        for i in range(5):
            button = ctk.CTkButton(
                master=self.frame, text=button_texts[i], font=buttonfont,
                fg_color=button_colors[i], text_color="#ffffff",  # White text
                width=900, height=80, command=button_commands[i], corner_radius=15
            )
            button.place(relx=0.5, rely=0.3 + (i * 0.125), anchor=tk.CENTER)

        #simple about page for user to read
        about_btn = ctk.CTkButton(
            master=self.frame, text="About", font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=150, height=60, fg_color="#0f606b", text_color="white",
            command=about_function, corner_radius=15
        )
        about_btn.place(relx=0.90, rely=0.95, anchor=tk.CENTER)  # Centered at bottom

        # "EXIT" button at the bottom
        exit_btn = ctk.CTkButton(
            master=self.frame, text="EXIT", font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=120, height=60, fg_color="#d9534f", text_color="white",
            command=exit_button, corner_radius=15
        )
        exit_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  # Centered at bottom

    def destroy(self):
        self.frame.destroy()
