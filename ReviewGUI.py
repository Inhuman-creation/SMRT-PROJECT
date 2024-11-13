# =====================
# ReviewGUI.py
# Latest version: Nov 11
# Review Mode
# =====================

import customtkinter as ctk
import tkinter as tk

#from ChoiceGUI import ChoiceGUI
#from Word import Word
from functools import partial
import random
import Settings
from WalkingWindow import WalkingWindow
#import os

'''************************* EXPERIMENTAL GUI IMPLEMENTATION *************************'''
#in this file I have just attempted to combine ChoiceGUI and TextGui together with significant reorganization
#TODO NEED TO MAKE A REVIEW_WINDOW or modify study_window TO ONLY PROVIDE KNOWN WORDS


class ReviewGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.frame = None
        self.controller.review_window = WalkingWindow(size=Settings.WALKING_WINDOW_SIZE)
        #TODO define the review window as only known words

        # Initialize fonts (all "Garet")
        self.flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        self.buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        self.backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        self.feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        self.show_random_card()

    def show_random_card(self):
        # Clean up previous frame if it exists
        if self.frame:
          self.frame.destroy()

        #create frame for GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        #Randomly display ChoiceGUI or TextGUI
        if random.choice(["choice", "text"]) == "choice":
            self.create_multiple_choice()
        else:
            self.create_text_response()

    def create_multiple_choice(self):
        # Select flashword and choices
        flashword = self.controller.review_window.get_random_words(1)[0]
        choices = self.controller.review_window.get_random_words(4)
        random.shuffle(choices)

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        def mark_known():
            self.controller.review_window.mark_word_as_known(flashword)
            self.show_random_card()

        def display_feedback(answer_word):
            feedback_text = ""
            feedback_color = "#f37d59"

            if answer_word == flashword:
                feedback_text = "🎉 Correct! 🎉"
                feedback_color = "#77721f"
            else:
                feedback_text = f"Incorrect.\n{flashword.foreign} means {flashword.english.lower()}"

            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="white",
                font=self.feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
            )
            feedback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.frame.after(2000, self.show_random_card)

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.foreign, text_color="black",
            font=self.flashfont, fg_color=None
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.3, anchor=tk.CENTER)

        # Create multiple choice buttons
        for idx, choice in enumerate(choices):
            choice_button = ctk.CTkButton(
                master=self.frame, text=choice.english, text_color="white",
                font=self.buttonfont, command=partial(display_feedback, choice)
            )
            choice_button.place(relx=0.3 + (idx % 2) * 0.4, rely=0.6 + (idx // 2) * 0.15, relwidth=0.3, relheight=0.1)

        # Create control buttons
        self.create_control_buttons(back_function, mark_known)

    def create_text_response(self):
        flashword = self.controller.review_window.get_random_words(1)[0]

        def back_function():
            self.controller.show_menu_gui()

        def mark_known():
            self.controller.review_window.mark_word_as_known(flashword)
            self.show_random_card()

        def display_feedback(_):
            word = text_entry.get()
            feedback_text = ""
            feedback_color = "#f37d59"

            if self.controller.review_window.check_word_definition(flashword, word):
                feedback_text = "🎉 Correct! 🎉"
                feedback_color = "#77721f"
            else:
                feedback_text = f"Incorrect.\n{flashword.foreign} means {flashword.english.lower()}"

            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="white",
                font=self.feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
            )
            feedback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.frame.after(2000, self.show_random_card)

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.foreign, text_color="black",
            font=self.flashfont, fg_color=None
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.3, anchor=tk.CENTER)

        # Create text entry
        text_entry = ctk.CTkEntry(
            master=self.frame, placeholder_text="Type translation here...",
            font=self.buttonfont, fg_color="white", border_color="lightgray", border_width=2, text_color="black"
        )
        text_entry.place(relx=0.5, rely=0.6, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)
        text_entry.bind("<Return>", display_feedback)

        # Create submit button
        submit_button = ctk.CTkButton(
            master=self.frame, text="Submit", text_color="white",
            font=self.buttonfont, command=partial(display_feedback, None)
        )
        submit_button.place(relx=0.5, rely=0.75, relwidth=0.3, relheight=0.2, anchor=tk.CENTER)

        # Create control buttons
        self.create_control_buttons(back_function, mark_known)

    def create_control_buttons(self, back_function, mark_known):
        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=self.backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

        # Create known word button
        known_word_button = ctk.CTkButton(
            master=self.frame, text="Already\nKnow", font=self.backbuttonfont,
            width=600, height=200, command=mark_known,
            fg_color="#0f606b", text_color="white", corner_radius=20
        )
        known_word_button.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
