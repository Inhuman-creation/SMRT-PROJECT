"""
ChoiceGUI.py
================
This is the GUI for the "Multiple Choice
Flashcards" screen. There are four selections for
the user to select from, as well as an "already know"
button, TTS button, BACK button, sound effects for right
and wrong answers, and corrective feedback if needed.

Version: 4.0
Since: 11-17-2024
"""

import customtkinter as ctk
import tkinter as tk
from TextToSpeech import play_pronunciation
import Settings
from Word import Word
import random
from functools import partial
import logging
from PIL import Image
import pygame


class ChoiceGUI:
    """
    This class contains the GUI for the multiple choice flashcards.
    """

    def __init__(self, controller):
        """
        Initializes the GUI and sets up the layout, flashcard, and interactive elements.
        """
        # Store the controller and app for use in the GUI
        self.controller = controller

        # Set the volume multiplier for sound effects
        self.app = controller.app
        self.volume_mult = 0.5

        # Initialize variables for GUI display

        # Get a random set of four words, including the flashcard word
        flashword, var1, var2, var3 = self.controller.study_window.get_random_words(4)

        # Store the flashcard word and other choices
        self.flashword = flashword  # Store the word for later use
        self.choices = [var1, var2, var3]  # put into list to make them able to be looped over (iterable)

        # Randomly decide the position of the correct answer in the choices
        self.answer_position = random.randint(0, 3)
        self.choices.insert(self.answer_position, self.flashword)

        # Log the multiple-choice options
        logging.info(f"MULTIPLE CHOICE OPTIONS: {self.choices}")

        # Create the main frame for the GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Create custom fonts for various text elements
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")  # Even larger font for flashcard
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")  # Smaller font for feedback text
        buttonfont = ctk.CTkFont(family="Garet", size=55, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")

        # List of supportive messages for correct answers
        supportive_messages = [
            "You got this!", "You're on a roll!", "Amazing!", "Well done!", "Keep going!", "Perfect!",
            "One step closer!", "Flawless!", "You're a natural!"
        ]

        # Define GUI functions


        def back_function():
            """
            Returns the user to the main menu GUI.
            """
            self.controller.show_menu_gui()

        def mark_known():
            """
            Marks the current flashcard word as known and moves to the next word.
            """
            self.controller.study_window.mark_word_as_known(flashword)
            switch_to_next_word()

        def text_to_speech_function(word):
            """
            Plays the pronunciation of the given word using text-to-speech.
            """
            if Settings.FOREIGN_TO_ENGLISH:
                play_pronunciation(word.foreign, Settings.LANGUAGE)
            else:
                play_pronunciation(word.english, "english")

        def switch_to_next_word():
            """
            Loads a new set of random words and updates the GUI.
            """
            flashword, var1, var2, var3 = self.controller.study_window.get_random_words(4)
            self.flashword = flashword
            self.choices = [var1, var2, var3]
            self.answer_position = random.randint(0, 3)
            self.choices.insert(self.answer_position, self.flashword)
            self.controller.show_choice_gui()

        def hide_feedback(feedback_label, feedback_button, buttons):
            """
            Hides feedback, re-enables buttons, and moves to the next word.
            """
            feedback_label.destroy()
            if feedback_button:
                feedback_button.destroy()
            for btn in buttons:
                btn.configure(state="normal")
            switch_to_next_word()

        def display_feedback(word: Word):
            """
            Displays feedback for the user's answer, indicating correctness.
            Plays sound effects and disables buttons until the next word is loaded.
            """
            # Default incorrect color
            feedback_color = "#f37d59"

            # If the response is correct...
            if self.controller.study_window.check_word_definition(self.flashword, word):
                # Random supportive message
                feedback_text = random.choice(supportive_messages)
                # Correct color
                feedback_color = "#77721f"
                # Create feedback label for correct answer
                feedback_label = ctk.CTkLabel(
                    master=self.frame,
                    text=feedback_text,
                    text_color="white",
                    font=feedbackfont,
                    fg_color=feedback_color,
                    wraplength=400,
                    justify="center",
                    corner_radius=5
                )
                feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

                # Play sound effect for correct answer
                sound = pygame.mixer.Sound("assets/correct.wav")
                sound.set_volume((Settings.VOLUME/100) * self.volume_mult)
                sound.play()

                # Disable all choice buttons after a guess is made
                for btn in buttons:
                    btn.configure(state="disabled")
                self.known_word_button.configure(state="disabled")

                # Automatically hide feedback and switch to the next word after 2 seconds
                self.frame.after(1000, hide_feedback, feedback_label, None, buttons)

            # If the answer is wrong...
            else:
                # Print the correct response
                feedback_text = "Not quite! {} means {}.".format(self.flashword.foreign, self.flashword.english.lower()) \
                    if Settings.FOREIGN_TO_ENGLISH else f"Not quite! {self.flashword.english.lower()} translates to {self.flashword.foreign}"

                # Display corrective feedback
                feedback_label = ctk.CTkLabel(
                    master=self.frame,
                    text=feedback_text,
                    text_color="white",
                    font=feedbackfont,
                    fg_color=feedback_color,
                    wraplength=400,
                    justify="center",
                    corner_radius=5
                )
                feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

                # Play sound effect for wrong answer
                sound = pygame.mixer.Sound("assets/incorrect.wav")
                sound.set_volume((Settings.VOLUME/100) * self.volume_mult)
                sound.play()

                # Disable all choice buttons after a guess is made
                for btn in buttons:
                    btn.configure(state="disabled")
                self.known_word_button.configure(state="disabled")

                # Create OK button for incorrect answers
                feedback_button = ctk.CTkButton(
                    master=self.frame,
                    text="OK",
                    font=buttonfont,
                    width=160,
                    height=100,
                    command=lambda: hide_feedback(feedback_label, feedback_button, buttons),
                    fg_color="#d9534f",
                    text_color="white",
                    corner_radius=5
                )
                feedback_button.place(relx=0.5, rely=0.7, relwidth=0.1, relheight=0.08,
                                      anchor=tk.CENTER)

        # Word in foreign lang
        flashcard = ctk.CTkLabel(
            master=self.frame, text=self.flashword.foreign if Settings.FOREIGN_TO_ENGLISH else self.flashword.english.lower(),
            text_color="black",
            font=flashfont, fg_color=None  # Remove background color
        )
        flashcard.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Define a function to wrap text if it is too long for the multiple choice button
        def wrap_text(text, max_length=30):
            """
            Wraps the text to a new line if it exceeds max_length.
            Inserts a newline character at spaces to prevent breaking words.
            """
            if len(text) > max_length:
                wrapped_text = ""
                current_line_length = 0
                for word in text.split():
                    if current_line_length + len(word) + 1 > max_length:
                        wrapped_text += "\n"  # Start a new line
                        current_line_length = 0
                    elif current_line_length > 0:
                        wrapped_text += " "  # Add space between words
                        current_line_length += 1
                    wrapped_text += word
                    current_line_length += len(word)
                return wrapped_text
            return text

        # Create multiple choice buttons with white text and hover effect
        buttons = []
        for i in range(4):
            choice_text = self.choices[i].english.lower() if Settings.FOREIGN_TO_ENGLISH else self.choices[i].foreign
            wrapped_text = wrap_text(choice_text, max_length=25)  # Adjust max_length as needed for line length
            button = ctk.CTkButton(
                master=self.frame,
                text = wrapped_text,
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

        # Back button
        back_icon = ctk.CTkImage(light_image=Image.open("Assets/back-icon.png"), size=(30, 30))
        exit_button = ctk.CTkButton(
            master=self.frame,
            text="BACK",
            font=backbuttonfont,
            width=120,
            height=60,
            command=back_function,
            fg_color="#d9534f",
            text_color="white",
            corner_radius=15,
            image=back_icon,
            compound="left"
        )
        exit_button.place(relx=0.055, rely=0.06, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Known word button
        known_icon = ctk.CTkImage(light_image=Image.open("Assets/known-icon.png"), size=(30, 30))
        self.known_word_button = ctk.CTkButton(
            master=self.frame,
            text="Already\nKnow",
            font=backbuttonfont,
            width=160,
            height=80,
            command=mark_known,
            fg_color="#0f606b",
            text_color="white",
            corner_radius=20,
            image=known_icon,
            compound="left"
        )
        self.known_word_button.place(relx=0.93, rely=0.06, relwidth=0.13, relheight=0.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_icon = ctk.CTkImage(light_image=Image.open("Assets/tts-icon.png"), size=(30, 30))
        tts_button = ctk.CTkButton(
            master=self.frame,
            text="Speak\nText",
            font=backbuttonfont,
            width=160,
            height=80,
            command=lambda: text_to_speech_function(self.flashword),
            fg_color="#0f606b",
            text_color="white",
            corner_radius=20,
            image=tts_icon,
            compound="left"
        )
        tts_button.place(relx=0.93, rely=0.18, relwidth=0.13, relheight=0.1, anchor=tk.CENTER)

        # Automatically trigger text-to-speech if enabled in settings
        if Settings.AUTO_TTS:
            text_to_speech_function(self.flashword)

    def destroy(self):
        self.frame.destroy()