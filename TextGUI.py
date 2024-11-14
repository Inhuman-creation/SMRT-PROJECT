# =====================
# TextGUI.py
# Latest version: Nov 11 2024
# Text Input flashcards screen
# =====================

import customtkinter as ctk
import tkinter as tk
from Word import Word
from functools import partial
import random
from TextToSpeech import play_pronunciation
import Settings


class TextGUI:
    """
    This class contains the GUI for the text-input flashcards.
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword = self.controller.study_window.get_random_words(1)[0]

        # Create frame for  GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")  # from choice GUI
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)  # Ensure frame occupies full screen

        # Create fonts (all "Garet")
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")  # Reduced the size for submit button
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")  # Smaller font for feedback text

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        def mark_known():
            self.controller.study_window.mark_word_as_known(flashword)
            self.controller.show_text_gui()

        def text_to_speech_function(word):
            play_pronunciation(word.foreign, Settings.LANGUAGE)

        def switch_to_next_word():  # Function to switch to the next word
            self.controller.show_text_gui()

        def hide_feedback(feedback_label, feedback_button, buttons):  # Function to hide feedback and re-enable buttons
            feedback_label.destroy()
            if feedback_button:
                feedback_button.destroy()
            '''for btn in buttons:
                btn.configure(state="normal")  # Re-enable buttons'''
            # Immediately switch to the next word after the feedback disappears
            switch_to_next_word()

        def display_feedback(_):  # _ is an unused arg passed from CTkEntry.bind()
            word = text_entry.get()
            feedback_text = ""
            feedback_color = "#f37d59"  # from choice GUI

            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="white",
                font=feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
            )
            feedback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            if self.controller.study_window.check_word_definition(flashword, word):
                feedback_text = "🎉 Correct! 🎉"
                feedback_color = "#77721f"  # Correct color

                # Automatically hide feedback and switch to the next word after 2 seconds
                self.frame.after(500, hide_feedback, feedback_label, None, None)  # No button for correct answer

            else:
                feedback_text = "Incorrect.\n{} means {}".format(flashword.foreign, flashword.english.lower())
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, text_color="white",
                font=feedbackfont, fg_color=feedback_color, wraplength=400, justify="center", corner_radius=25
            )
            feedback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            feedback_button = ctk.CTkButton(
                master=self.frame, text="OK", font=buttonfont,
                width=160, height=100, command=self.controller.show_text_gui,
                fg_color="#ffc24a", text_color="white", corner_radius=20  # from choice GUI feedback button
            )
            feedback_button.place(relx=0.5, rely=0.67, relwidth=.1, relheight=.1, anchor=tk.CENTER)

            # Disable Enter key and submit button after feedback
            text_entry.unbind("<Return>")
            submit_button.configure(state="disabled")

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.foreign, text_color="black",
            font=flashfont, fg_color=None  # from choice GUI
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)

        # Create and place the text entry (same as LoginGUI.py's text entry)
        text_entry = ctk.CTkEntry(
            master=self.frame, placeholder_text="Type translation here...",
            font=buttonfont,
            fg_color="white", border_color="lightgray", border_width=2, text_color="black"
        )
        text_entry.place(relx=0.5, rely=0.6, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)  # Matching width/height

        # Create and place submit button (made smaller font size)
        submit_button = ctk.CTkButton(
            master=self.frame,
            text="Submit", text_color="white",
            command=partial(display_feedback, None),
            font=buttonfont,
        )
        submit_button.place(relx=0.5, rely=0.75, relwidth=0.3, relheight=0.2, anchor=tk.CENTER)  # Smaller relwidth and relheight

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20  # from Choice GUI
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Known word button
        known_word_button = ctk.CTkButton(
            master=self.frame, text="Already\nKnow", font=backbuttonfont,
            width=600, height=200, command=mark_known
            ,
            fg_color="#0f606b", text_color="white", corner_radius=20  # White text and red color
        )
        known_word_button.place(relx=0.95, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_button = ctk.CTkButton(
            master=self.frame, text="Speak\nText", font=backbuttonfont,
            width=600, height=200, command=lambda: text_to_speech_function(flashword),
            fg_color="#0f606b", text_color="white", corner_radius=20  # White text and red color
        )
        tts_button.place(relx=0.95, rely=0.2, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Auto TTS if desired
        if Settings.AUTO_TTS:
            text_to_speech_function(flashword)

    def destroy(self):
        self.frame.destroy()
