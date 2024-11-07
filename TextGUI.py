# choiceGUI.py

import customtkinter as ctk
import tkinter as tk
from Word import Word
from functools import partial
import random


class TextGUI:
    """
    This class contains the GUI for the text-input flashcards.
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword = self.controller.study_window.get_random_words(1)[0]

        # Create frame for choice GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000)
        self.frame.pack(expand=1, fill="both")

        # Create fonts
        flashfont = ctk.CTkFont(family="Times New Roman", size=75, weight="bold")
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Times New Roman", size=25, weight="bold")

        # button functions
        def back_function():
            self.controller.show_menu_gui()

        def display_feedback(_):  # _ is an unused arg passed from CTkEntry.bind()
            word = text_entry.get()
            feedback_text = ""
            if self.controller.study_window.check_word_definition(flashword, word):
                feedback_text = "🎉 Correct! 🎉"
            else:
                feedback_text = "Incorrect.\n{} means {}".format(flashword.spanish, flashword.english.lower())
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="black",
                font=flashfont, fg_color="grey75"
            )
            feedback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            feedback_button = ctk.CTkButton(
                master=self.frame, text="OK", font=buttonfont,
                width=160, height=100, command=self.controller.show_text_gui,
                fg_color="#000080"
            )
            feedback_button.place(relx=0.5, rely=0.67, relwidth=.1, relheight=.1, anchor=tk.CENTER)
            # TODO: update relevant count variables before displaying the feedback

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.spanish, text_color="black",
            font=flashfont, fg_color="grey75"
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)

        # Creat frame to hold text input field and submit button
        input_frame = ctk.CTkFrame(
            master=self.frame
        )
        input_frame.place(relx=0.5, rely=0.75, relwidth=0.5, relheight=0.3, anchor=tk.CENTER)

        # Create and place the text entry
        text_entry = ctk.CTkEntry(
            master=input_frame,
            placeholder_text="Translation",
            font=buttonfont
        )
        text_entry.place(relx=0.5, rely=0.25, relwidth=0.5, relheight=0.3, anchor=tk.CENTER)
        text_entry.bind("<Return>", display_feedback)  # submit by pressing Enter

        # Create and place submit button
        submit_button = ctk.CTkButton(
            master=input_frame,
            text="Submit",
            command=partial(display_feedback, None),
            font=buttonfont
        )
        submit_button.place(relx=0.5, rely=0.75, relwidth=0.5, relheight=0.3, anchor=tk.CENTER)

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="Back", font=backbuttonfont,
            width=100, height=50, command=back_function
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
