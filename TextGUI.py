# =====================
# TextGUI.py
# Latest version: Nov 15 2024
# Text Input flashcards screen
# =====================

import customtkinter as ctk
import tkinter as tk
from Word import Word
from functools import partial
import random
from TextToSpeech import play_pronunciation
import Settings
from PIL import Image
import pygame

class TextGUI:
    """
    This class contains the GUI for the text-input flashcards.
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword = self.controller.study_window.get_random_words(1)[0]

        # Create frame for GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        # Create fonts (all "Garet")
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        # Supportive messages for correct answers
        supportive_messages = [
            "You got this!", "You're on a roll!", "Amazing!", "Well done!", "Keep going!", "Perfect!",
            "One step closer!", "Flawless!", "You're a natural!"
        ]

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        def mark_known():
            self.controller.study_window.mark_word_as_known(flashword)
            self.controller.show_text_gui()

        def text_to_speech_function(word):
            play_pronunciation(word.foreign, Settings.LANGUAGE)

        def switch_to_next_word():
            self.controller.show_text_gui()

        def hide_feedback(feedback_label, feedback_button):
            feedback_label.destroy()
            if feedback_button:
                feedback_button.destroy()
            switch_to_next_word()

        def display_feedback(_):
            word = text_entry.get()
            feedback_text = ""

            # Set feedback color based on whether the answer is correct or incorrect
            if self.controller.study_window.check_word_definition(flashword, word):
                feedback_text = random.choice(supportive_messages)
                feedback_color = "#77721f"  # Correct color
            else:
                feedback_text = "Not quite!\n{} means {}".format(flashword.foreign, flashword.english.lower())
                feedback_color = "#f37d59"  # Incorrect color

            # Create feedback label
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="white",
                font=feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=5
            )
            feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

            # If the answer is correct, auto-hide feedback after 1 second
            if feedback_color == "#77721f":
                self.frame.after(1000, hide_feedback, feedback_label, None)  # Auto-hide after 1 second

                # Play sound effect for correct answer
                sound = pygame.mixer.Sound("assets/correct.wav")
                sound.play()

            # If the answer is wrong, show an "OK" button to dismiss the feedback
            else:
                feedback_button = ctk.CTkButton(
                    master=self.frame, text="OK", font=buttonfont,
                    width=160, height=100, command=lambda: hide_feedback(feedback_label, feedback_button),
                    fg_color="#d9534f", text_color="white", corner_radius=5
                )
                feedback_button.place(relx=0.5, rely=0.62, relwidth=0.1, relheight=0.08, anchor=tk.CENTER)

                # Play sound effect for incorrect answer
                sound = pygame.mixer.Sound("assets/incorrect.wav")
                sound.play()

            text_entry.unbind("<Return>")
            submit_button.configure(state="disabled")

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.foreign, text_color="black",
            font=flashfont, fg_color=None
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)

        text_entry = ctk.CTkEntry(
            master=self.frame, placeholder_text="Type translation here...",
            font=ctk.CTkFont(family="Garet", size=45, weight="normal"),
            fg_color="#f1dfb6", border_width=2, text_color="black",
            placeholder_text_color="#bdb091",
            corner_radius=16, justify="center", border_color="#bdb091"
        )
        text_entry.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.08, anchor=tk.CENTER)
        text_entry.bind("<Return>", display_feedback)

        submit_icon = ctk.CTkImage(light_image=Image.open("Assets/submit-icon.png"), size=(40, 40))
        submit_button = ctk.CTkButton(
            master=self.frame, text="Submit", text_color="white",
            command=partial(display_feedback, None),
            font=buttonfont, fg_color="#0f606b", corner_radius=20,
            image=submit_icon, compound="left"
        )
        submit_button.place(relx=0.5, rely=0.75, relwidth=0.2, relheight=0.1, anchor=tk.CENTER)

        # Back button
        back_icon = ctk.CTkImage(light_image=Image.open("Assets/back-icon.png"), size=(30, 30))
        exit_button = ctk.CTkButton(
            master=self.frame, text="BACK", font=backbuttonfont,
            width=120, height=60, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=15,  # White text and red color
            image=back_icon, compound="left"
        )
        exit_button.place(relx=0.055, rely=0.06, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Known word button
        known_icon = ctk.CTkImage(light_image=Image.open("Assets/known-icon.png"), size=(30, 30))
        self.known_word_button = ctk.CTkButton(
            master=self.frame, text="Already\nKnow", font=backbuttonfont,
            width=160, height=80, command=mark_known,
            fg_color="#0f606b", text_color="white", corner_radius=20,
            image=known_icon, compound="left"
        )
        self.known_word_button.place(relx=0.93, rely=0.06, relwidth=0.13, relheight=0.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_icon = ctk.CTkImage(light_image=Image.open("Assets/tts-icon.png"), size=(30, 30))
        tts_button = ctk.CTkButton(
            master=self.frame, text="Speak\nText", font=backbuttonfont,
            width=160, height=80, command=lambda: text_to_speech_function(flashword),
            fg_color="#0f606b", text_color="white", corner_radius=20,
            image=tts_icon, compound="left"
        )
        tts_button.place(relx=0.93, rely=0.18, relwidth=0.13, relheight=0.1, anchor=tk.CENTER)

        if Settings.AUTO_TTS:
            text_to_speech_function(flashword)

    def destroy(self):
        self.frame.destroy()