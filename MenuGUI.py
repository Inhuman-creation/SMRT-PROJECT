# menuGUI.py

import customtkinter as ctk
import tkinter as tk


class MenuGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000)
        self.frame.pack(expand=1, fill="both")

        # Create button font
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")

        # Button functions
        def choice_function():
            self.controller.show_choice_gui()

        def text_function():
            self.controller.show_text_gui()

        def placeholder_function():
            print("Placeholder function")

        def exit_button():
            print("Exiting application")
            self.app.destroy()

        # Create buttons
        start = ctk.CTkButton(
            master=self.frame, text="Multiple Choice \nFlashcards", font=buttonfont,
            width=350, height=200, command=choice_function
        )
        start.place(relx=0.5, rely=0.12, relwidth=.3, relheight=.2, anchor=tk.CENTER)

        placeholder1 = ctk.CTkButton(
            master=self.frame, text="Text-Input \nFlashcards", font=buttonfont,
            width=350, height=200, command=text_function
        )
        placeholder1.place(relx=0.5, rely=0.35, relwidth=.3, relheight=.2, anchor=tk.CENTER)

        placeholder2 = ctk.CTkButton(
            master=self.frame, text="Statistics", font=buttonfont,
            width=350, height=200, command=placeholder_function
        )
        placeholder2.place(relx=0.5, rely=0.58, relwidth=.3, relheight=.2, anchor=tk.CENTER)

        exit_btn = ctk.CTkButton(
            master=self.frame, text="Exit", font=buttonfont,
            width=350, height=200, command=exit_button
        )
        exit_btn.place(relx=0.5, rely=0.81, relwidth=.3, relheight=.2, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
