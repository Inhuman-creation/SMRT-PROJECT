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
from TextToSpeech import play_pronunciation

'''************************* EXPERIMENTAL GUI IMPLEMENTATION *************************'''
#in this file I have combined ChoiceGUI and TextGui together with significant reorganization


class ReviewGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.frame = None

        #pull all known words out of the dictionary
        self.review_window = [word for word in self.controller.study_window.words_dict.values() if word.is_known]

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
        if len(self.review_window) == 0:
            #no words to review
            self.show_no_review_words_error()
        elif len(self.review_window) < 4:
            #not enough words for multiple choice
            self.create_text_response()
        elif random.choice(["choice", "text"]) == "choice":
            self.create_multiple_choice()
        else:
            self.create_text_response()

    def show_no_review_words_error(self):
        #create message to show there are no words to review
        feedback_color = "#f37d59"
        no_review_label = ctk.CTkLabel(
            master=self.frame, text="No words to review",
            font=self.feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
        )
        no_review_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def back_function():
            self.controller.show_menu_gui()

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=self.backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

    def create_multiple_choice(self):
        # Select flashword and choices
        flashword, var1, var2, var3 = self.get_random_words(4)
        flashword = flashword  # Store the word for later use
        choices = [flashword, var1, var2, var3]  # put into list to shuffle
        random.shuffle(choices)

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        def text_to_speech_function(word):
            if Settings.FOREIGN_TO_ENGLISH:
                play_pronunciation(word.foreign, Settings.LANGUAGE)
            else:
                play_pronunciation(word.english, "english")

        def display_feedback(answer_word):
            feedback_text = ""
            feedback_color = "#f37d59"

            if flashword.check_definition(answer_word):
                feedback_text = "🎉 Correct! 🎉"
                feedback_color = "#77721f"
            else:
                feedback_text = "Not quite!\n{} means {}.".format(flashword.foreign, flashword.english.lower()) \
                    if Settings.FOREIGN_TO_ENGLISH else f"Not quite!\n{flashword.english.lower()} translates to {flashword.foreign}"

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
        buttons = []
        for i in range(4):
            button = ctk.CTkButton(
                master=self.frame,
                text=choices[i].english.lower() if Settings.FOREIGN_TO_ENGLISH else choices[i].foreign,
                font=self.buttonfont,
                width=480, height=250, text_color="#ffffff",  # Set font color to white
                command=partial(display_feedback, choices[i]),
                fg_color="#acb87c", hover_color="#77721f", corner_radius=20
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

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=self.backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_button = ctk.CTkButton(
            master=self.frame, text="Speak\nText", font=self.backbuttonfont,
            width=600, height=200, command=lambda: text_to_speech_function(flashword),
            fg_color="#0f606b", text_color="white", corner_radius=20  # White text and red color
        )
        tts_button.place(relx=0.95, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Auto TTS if desired
        if Settings.AUTO_TTS:
            text_to_speech_function(flashword)

    def create_text_response(self):
        flashword = self.get_random_words(1)[0]

        def back_function():
            self.controller.show_menu_gui()

        def text_to_speech_function(word):
            play_pronunciation(word.foreign, Settings.LANGUAGE)

        def display_feedback(_):
            word = text_entry.get()
            feedback_text = ""
            feedback_color = "#f37d59"

            if flashword.check_definition(word):
                feedback_text = "🎉 Correct! 🎉"
                feedback_color = "#77721f"
            else:
                feedback_text = "Not quite!\n{} means {}.".format(flashword.foreign, flashword.english.lower())

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

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=self.backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_button = ctk.CTkButton(
            master=self.frame, text="Speak\nText", font=self.backbuttonfont,
            width=600, height=200, command=lambda: text_to_speech_function(flashword),
            fg_color="#0f606b", text_color="white", corner_radius=20  # White text and red color
        )
        tts_button.place(relx=0.95, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Auto TTS if desired
        if Settings.AUTO_TTS:
            text_to_speech_function(flashword)

    def destroy(self):
        self.frame.destroy()

    def get_random_words(self, count: int) -> list:
        """
        Return a random selection of unique words from the review window
        Will not return more current_words than can be stored in the review window
        Will return an empty list if review window is empty

        param: count int : The number of random words to return
        return: A list of randomly selected Word objects
        """

        return random.sample(self.review_window, min(count, len(self.review_window))) if self.review_window else []