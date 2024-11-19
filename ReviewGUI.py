"""
ReviewGUI.py
================
This is the GUI for the Review screen. The
user will be prompted to practice their
known words, through multiple choice
and text-based input

Version: 4.0
Since: 11-17-2024
"""

import customtkinter as ctk
import tkinter as tk
from functools import partial
import random
import Settings
from TextToSpeech import play_pronunciation
from PIL import Image

class ReviewGUI:
    """
    This class contains the GUI for the review page.
    """
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app
        self.frame = None

        # Pull all known words out of the dictionary
        self.review_window = [word for word in self.controller.study_window.words_dict.values() if word.is_known]

        # Initialize fonts (all "Garet")
        self.flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        self.buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        self.backbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        self.feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        self.show_random_card()

    def show_random_card(self):
        # Clean up previous frame if it exists
        if self.frame:
          self.frame.destroy()

        # Create frame for GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        def back_function():
            self.controller.show_menu_gui()

        # Back button
        back_icon = ctk.CTkImage(light_image=Image.open("Assets/back-icon.png"), size=(30, 30))
        exit_button = ctk.CTkButton(
            master=self.frame,
            text="BACK",
            font=self.backbuttonfont,
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

        # Randomly display ChoiceGUI or TextGUI
        if len(self.review_window) == 0:
            # Tell the user there are no words to review
            self.show_no_review_words_error()
        elif len(self.review_window) < 4:
            # Not enough words for multiple choice
            self.create_text_response()
        elif random.choice(["choice", "text"]) == "choice":
            self.create_multiple_choice()
        else:
            self.create_text_response()

    def show_no_review_words_error(self):
        # Create message to show there are no words to review
        feedback_color = "#f37d59"
        no_review_label = ctk.CTkLabel(
            master=self.frame,
            text="No words to review!",
            font=self.feedbackfont,
            fg_color=feedback_color,
            wraplength=400,
            justify="center",
            corner_radius=25
        )
        no_review_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_multiple_choice(self):
        # Select flashword and choices
        flashword, var1, var2, var3 = self.get_random_words(4)
        flashword = flashword  # Store the word for later use
        choices = [flashword, var1, var2, var3]  # Put into list to shuffle
        random.shuffle(choices)

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        # Text to speech function
        def text_to_speech_function(word):
            if Settings.FOREIGN_TO_ENGLISH:
                play_pronunciation(word.foreign, Settings.LANGUAGE)
            else:
                play_pronunciation(word.english, "english")

        def display_feedback(answer_word):
            # Default incorrect color
            feedback_color = "#f37d59"

            # Supportive messages for correct answers
            supportive_messages = [
                "You got this!", "You're on a roll!", "Amazing!", "Well done!", "Keep going!", "Perfect!",
                "One step closer!", "Flawless!", "You're a natural!"
            ]

            # Function to hide feedback and re-enable buttons
            def hide_feedback(feedback_label, feedback_button, buttons):
                feedback_label.destroy()
                if feedback_button:
                    feedback_button.destroy()
                for btn in buttons:
                    btn.configure(state="normal")  # Re-enable buttons

                # Immediately switch to the next word after the feedback disappears
                self.show_random_card()

            if flashword.check_definition(answer_word):
                # Random supportive message
                feedback_text = random.choice(supportive_messages)
                # Correct color
                feedback_color = "#77721f"
                # Create feedback label for correct answer
                feedback_label = ctk.CTkLabel(
                    master=self.frame,
                    text=feedback_text,
                    text_color="white",
                    font=self.feedbackfont,
                    fg_color=feedback_color,
                    wraplength=800,
                    justify="center",
                    corner_radius=5
                )
                feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

                # Disable all choice buttons after a guess is made
                for btn in buttons:
                    btn.configure(state="disabled")

                # Automatically hide feedback and switch to the next word after 1 second
                self.frame.after(1000, hide_feedback, feedback_label, None, buttons)
            else:
                # Provide the correct translation for the user
                feedback_text = "Not quite! {} means {}.".format(flashword.foreign, flashword.english.lower()) \
                    if Settings.FOREIGN_TO_ENGLISH else f"Not quite! {flashword.english.lower()} translates to {flashword.foreign}"

                feedback_label = ctk.CTkLabel(
                    master=self.frame,
                    text=feedback_text,
                    text_color="white",
                    font=self.feedbackfont,
                    fg_color=feedback_color,
                    wraplength=800,
                    justify="center",
                    corner_radius=5
                )
                feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

                # Disable all choice buttons after a guess is made
                for btn in buttons:
                    btn.configure(state="disabled")

                # Create OK button for incorrect answers
                feedback_button = ctk.CTkButton(
                    master=self.frame,
                    text="OK",
                    font=self.buttonfont,
                    width=160,
                    height=100,
                    command=lambda: hide_feedback(feedback_label, feedback_button, buttons),
                    fg_color="#d9534f",
                    text_color="white",
                    corner_radius=5
                )
                feedback_button.place(relx=0.5, rely=0.7, relwidth=0.1, relheight=0.08,
                                      anchor=tk.CENTER)

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame,
            text=flashword.foreign,
            text_color="black",
            font=self.flashfont,
            fg_color=None
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
            x = -1
            y = -1
            if i % 2 == 1:  # X values
                x = 0.25  # First and third buttons
            else:
                x = 0.75  # Second and fourth buttons

            if i < 2:  # Y values
                y = 0.58  # First and second buttons
            else:
                y = 0.85  # Third and fourth buttons
            buttons[i].place(relx=x, rely=y, relwidth=0.4, relheight=.25, anchor=tk.CENTER)

        # Text-to-speech button
        tts_icon = ctk.CTkImage(light_image=Image.open("Assets/tts-icon.png"), size=(30, 30))
        tts_button = ctk.CTkButton(
            master=self.frame,
            text="Speak\nText",
            font=self.backbuttonfont,
            width=160,
            height=80,
            command=lambda: text_to_speech_function(flashword),
            fg_color="#0f606b",
            text_color="white",
            corner_radius=20,
            image=tts_icon,
            compound="left"
        )
        tts_button.place(relx=0.93, rely=0.06, relwidth=0.13, relheight=0.1, anchor=tk.CENTER)

        # Auto TTS if desired
        if Settings.AUTO_TTS:
            text_to_speech_function(flashword)

    # Feedback for user based on their response
    def create_text_response(self):
        flashword = self.get_random_words(1)[0]

        # Play pronunciation (text to speech)
        def text_to_speech_function(word):
            play_pronunciation(word.foreign, Settings.LANGUAGE)

        # Displaying feedback
        def display_feedback(_):
            word = text_entry.get()
            feedback_text = ""

            # Supportive messages for correct answers
            supportive_messages = [
                "You got this!", "You're on a roll!", "Amazing!", "Well done!", "Keep going!", "Perfect!",
                "One step closer!", "Flawless!", "You're a natural!"
            ]

            def hide_feedback(feedback_label, feedback_button):
                feedback_label.destroy()
                if feedback_button:
                    feedback_button.destroy()
                self.show_random_card()

            # Set feedback color based on whether the answer is correct or incorrect
            if flashword.check_definition(word):
                feedback_text = random.choice(supportive_messages)
                feedback_color = "#77721f"  # Correct color
            else:
                feedback_text = "Not quite! {} means {}".format(flashword.foreign, flashword.english.lower())
                feedback_color = "#f37d59"  # Incorrect color

            # Create feedback label
            feedback_label = ctk.CTkLabel(
                master=self.frame,
                text=feedback_text,
                text_color="white",
                font=self.feedbackfont,
                fg_color=feedback_color,
                wraplength=800,
                justify="center",
                corner_radius=5
            )
            feedback_label.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.2, anchor=tk.CENTER)

            # If the answer is correct, auto-hide feedback after 1 second
            if feedback_color == "#77721f":
                self.frame.after(1000, hide_feedback, feedback_label, None)  # Auto-hide after 1 second

            # If the answer is wrong, show an "OK" button to dismiss the feedback
            else:
                feedback_button = ctk.CTkButton(
                    master=self.frame,
                    text="OK",
                    font=self.buttonfont,
                    width=160,
                    height=100,
                    command=lambda: hide_feedback(feedback_label, feedback_button),
                    fg_color="#d9534f",
                    text_color="white",
                    corner_radius=5
                )
                feedback_button.place(relx=0.5, rely=0.7, relwidth=0.1, relheight=0.08, anchor=tk.CENTER)

            text_entry.unbind("<Return>")
            submit_button.configure(state="disabled")

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame,
            text=flashword.foreign,
            text_color="black",
            font=self.flashfont,
            fg_color=None
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.3, anchor=tk.CENTER)

        # Create text entry field
        text_entry = ctk.CTkEntry(
            master=self.frame,
            placeholder_text="Type translation here...",
            font=ctk.CTkFont(family="Garet", size=45, weight="normal"),
            fg_color="#f1dfb6",
            border_width=2,
            text_color="black",
            placeholder_text_color="#bdb091",
            corner_radius=16,
            justify="center",
            border_color="#bdb091"
        )
        text_entry.place(relx=0.5, rely=0.6, relwidth=0.8, relheight=0.08, anchor=tk.CENTER)
        text_entry.bind("<Return>", display_feedback)

        # Submit button
        submit_icon = ctk.CTkImage(light_image=Image.open("Assets/submit-icon.png"), size=(40, 40))
        submit_button = ctk.CTkButton(
            master=self.frame,
            text="Submit",
            text_color="white",
            command=partial(display_feedback, None),
            font=self.buttonfont,
            fg_color="#0f606b",
            corner_radius=20,
            image=submit_icon,
            compound="left"
        )
        submit_button.place(relx=0.5, rely=0.75, relwidth=0.2, relheight=0.1, anchor=tk.CENTER)

        # Text-to-speech button
        tts_icon = ctk.CTkImage(light_image=Image.open("Assets/tts-icon.png"), size=(30, 30))
        tts_button = ctk.CTkButton(
            master=self.frame,
            text="Speak\nText",
            font=self.backbuttonfont,
            width=160,
            height=80,
            command=lambda: text_to_speech_function(flashword),
            fg_color="#0f606b",
            text_color="white",
            corner_radius=20,
            image=tts_icon,
            compound="left"
        )
        tts_button.place(relx=0.93, rely=0.06, relwidth=0.13, relheight=0.1, anchor=tk.CENTER)

        # Auto TTS if desired
        if Settings.AUTO_TTS:
            text_to_speech_function(flashword)

    # Getting random words for review
    def get_random_words(self, count):
        if len(self.review_window) < count:
            return random.choices(self.review_window, k=count)
        return random.sample(self.review_window, count)

    def destroy(self):
        self.frame.destroy()
