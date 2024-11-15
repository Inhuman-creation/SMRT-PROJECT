# =====================
# ChoiceGUI.py
# Latest version: Nov 11
# Multiple choice flashcards screen
# =====================

import customtkinter as ctk
import tkinter as tk
from TextToSpeech import play_pronunciation

import Settings
from Word import Word
import random
from functools import partial
import logging


class ChoiceGUI:
    """
    This class contains the GUI for the multiple choice flashcards.
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword, var1, var2, var3 = self.controller.study_window.get_random_words(4)
        self.flashword = flashword  # Store the word for later use
        self.choices = [var1, var2, var3]  # put into list to make them able to be looped over (iterable)

        self.answer_position = random.randint(0, 3)  # determines where the right answer will be placed
        self.choices.insert(self.answer_position, self.flashword)
        logging.info(f"MULTIPLE CHOICE OPTIONS: {self.choices}")

        # Create frame for choice GUI with background color
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Create fonts with "Garet"
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")  # Even larger font for flashcard
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")  # Smaller font for feedback text
        buttonfont = ctk.CTkFont(family="Garet", size=55, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        # Supportive messages for correct answers
        supportive_messages = [
            "Correcto!", "You got this!", "You're on a roll!", "Perfecto!", "Well done!", "Keep going!"
        ]

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        def mark_known():
            self.controller.study_window.mark_word_as_known(flashword)
            switch_to_next_word()

        def text_to_speech_function(word):
            if Settings.FOREIGN_TO_ENGLISH:
                play_pronunciation(word.foreign, Settings.LANGUAGE)
            else:
                play_pronunciation(word.english, "english")

        def switch_to_next_word():  # Function to switch to the next word
            flashword, var1, var2, var3 = self.controller.study_window.get_random_words(4)
            self.flashword = flashword
            self.choices = [var1, var2, var3]
            self.answer_position = random.randint(0, 3)
            self.choices.insert(self.answer_position, self.flashword)
            self.controller.show_choice_gui()

        def hide_feedback(feedback_label, feedback_button, buttons):  # Function to hide feedback and re-enable buttons
            feedback_label.destroy()
            if feedback_button:
                feedback_button.destroy()
            for btn in buttons:
                btn.configure(state="normal")  # Re-enable buttons

            # Immediately switch to the next word after the feedback disappears
            switch_to_next_word()

        def display_feedback(word: Word):
            feedback_text = ""
            feedback_color = "#f37d59"  # Default incorrect color

            if self.controller.study_window.check_word_definition(self.flashword, word):
                feedback_text = random.choice(supportive_messages)  # Random supportive message
                feedback_color = "#77721f"  # Correct color
                # Create feedback label for correct answer
                feedback_label = ctk.CTkLabel(
                    master=self.frame, text=feedback_text, text_color="white",
                    font=feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
                )
                feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

                # Disable all choice buttons after a guess is made
                for btn in buttons:
                    btn.configure(state="disabled")
                self.known_word_button.configure(state="disabled")

                # Automatically hide feedback and switch to the next word after 2 seconds
                self.frame.after(500, hide_feedback, feedback_label, None, buttons)  # No button for correct answer
            else:
                feedback_text = "Not quite!\n{} means {}.".format(self.flashword.foreign, self.flashword.english.lower()) \
                    if Settings.FOREIGN_TO_ENGLISH else f"Not quite!\n{self.flashword.english.lower()} translates to {self.flashword.foreign}"

                feedback_label = ctk.CTkLabel(
                    master=self.frame, text=feedback_text, text_color="white",
                    font=feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
                )
                feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

                # Disable all choice buttons after a guess is made
                for btn in buttons:
                    btn.configure(state="disabled")
                self.known_word_button.configure(state="disabled")

                # Create OK button for incorrect answers
                feedback_button = ctk.CTkButton(
                    master=self.frame, text="OK", font=buttonfont,
                    width=160, height=100, command=lambda: hide_feedback(feedback_label, feedback_button, buttons),
                    fg_color="#ffc24a", text_color="white", corner_radius=20  # New background color and text color
                )
                feedback_button.place(relx=0.5, rely=0.62, relwidth=0.1, relheight=0.08,
                                      anchor=tk.CENTER)  # Adjusted rely to make it closer

        # Word in foreign lang
        flashcard = ctk.CTkLabel(
            master=self.frame, text=self.flashword.foreign if Settings.FOREIGN_TO_ENGLISH else self.flashword.english.lower(),
            text_color="black",
            font=flashfont, fg_color=None  # Remove background color
        )
        flashcard.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Create multiple choice buttons with white text and hover effect
        buttons = []
        for i in range(4):
            button = ctk.CTkButton(
                master=self.frame, text=self.choices[i].english.lower() if Settings.FOREIGN_TO_ENGLISH else self.choices[i].foreign,
                font=buttonfont,
                width=480, height=250, text_color="#ffffff",  # Set font color to white
                command=partial(display_feedback, self.choices[i]),
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

        # EXIT button
        exit_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20  # White text and red color
        )
        exit_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Known word button
        self.known_word_button = ctk.CTkButton(
            master=self.frame, text="Already\nKnow", font=backbuttonfont,
            width=600, height=200, command=mark_known
,
            fg_color="#0f606b", text_color="white", corner_radius=20  # White text and red color
        )
        self.known_word_button.place(relx=0.95, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_button = ctk.CTkButton(
            master=self.frame, text="Speak\nText", font=backbuttonfont,
            width=600, height=200, command=lambda: text_to_speech_function(self.flashword),
            fg_color="#0f606b", text_color="white", corner_radius=20  # White text and red color
        )
        tts_button.place(relx=0.95, rely=0.17, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        #Auto TTS if desired
        if Settings.AUTO_TTS:
            text_to_speech_function(self.flashword)

    def destroy(self):
        self.frame.destroy()
