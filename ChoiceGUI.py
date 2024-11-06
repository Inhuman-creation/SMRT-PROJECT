# choiceGUI.py

import customtkinter as ctk
import tkinter as tk
from Word import Word
import random
from functools import partial


class ChoiceGUI:
    """
    This class contains the GUI for the multiple choice flashcards.
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword, var1, var2, var3 = self.controller.study_window.get_random_words(4)
        choices = [var1, var2, var3]  # put into list to make them able to be looped over (iterable)
        answer_position = random.randint(0, 3)  # determines where the right answer will be placed
        choices.insert(answer_position, flashword)

        # Create frame for choice GUI with background color
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Create fonts with "Garet"
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")  # Even larger font for flashcard
        buttonfont = ctk.CTkFont(family="Garet", size=55, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")

        # button functions
        def back_function():
            self.controller.show_menu_gui()

        def display_feedback(word: Word):
            feedback_text = ""
            if flashword.check_definition_english(word.english):
                feedback_text = "🎉 Correct! 🎉"
            else:
                feedback_text = "Incorrect.\n{} means {}".format(flashword.spanish, flashword.english.lower())
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="black",
                font=flashfont, fg_color="grey75"
            )
            feedback_label.place(relx=0.5, rely=0.5, relwidth=.3, relheight=.2, anchor=tk.CENTER)
            feedback_button = ctk.CTkButton(
                master=self.frame, text="OK", font=buttonfont,
                width=160, height=100, command=self.controller.show_choice_gui,
                fg_color="#000080", corner_radius=20
            )
            feedback_button.place(relx=0.5, rely=0.65, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Create flashcard label without background color
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.spanish, text_color="black",
            font=flashfont, fg_color=None  # Remove background color
        )
        flashcard.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Create multiple choice buttons with white text and hover effect
        buttons = []
        for i in range(4):
            button = ctk.CTkButton(
                master=self.frame, text=choices[i].english.lower(), font=buttonfont,
                width=480, height=250, text_color="#ffffff",  # Set font color to white
                command=partial(display_feedback, choices[i]),
                fg_color="#acb87c", hover_color="#77721f", corner_radius=20
                # Apply color, hover effect, and rounded corners
            )
            buttons.append(button)

        # Place the buttons
        for i in range(4):
            x = -1  # init temporary position variables
            y = -1
            if i % 2 == 1:  # x values
                x = 0.25  # first and third buttons
            else:
                x = 0.75  # second and fourth

            if i < 2:  # y values
                y = 0.58  # first and second buttons
            else:
                y = 0.85  # third and fourth buttons
            buttons[i].place(relx=x, rely=y, relwidth=0.4, relheight=.25, anchor=tk.CENTER)

        # Create EXIT button with an intuitive color
        exit_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", corner_radius=20  # Set to a red color to indicate exit
        )
        exit_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
