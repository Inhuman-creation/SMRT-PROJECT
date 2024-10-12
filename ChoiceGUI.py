# choiceGUI.py

import customtkinter as ctk
import tkinter as tk
from Word import Word
import random
from functools import partial

class ChoiceGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword, var1, var2, var3 = self.controller.study_window.get_random_words(4)
        answer_position = random.randint(0, 3)  # determines where the right answer will be placed
        choices = [var1, var2, var3]  # put into list to make them looped over (iterable)
        choices.insert(answer_position, flashword)

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

        def display_feedback(word: Word):
            if flashword.check_definition(word.english):
                print("Correct\n")
            else:
                print("Incorrect")
                print("flashword:", flashword.english)
                print("word:", word.english)
                print()

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.spanish, text_color="black",
            font=flashfont, fg_color="grey75"
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)

        # Create multiple choice buttons
        buttons = []
        for i in range(4):
            buttons.append(
                ctk.CTkButton(
                    master=self.frame, text=choices[i].english.lower(), font=buttonfont,
                    width=480, height=250, command=partial(display_feedback, choices[i]) 
                    # the use of partial() allows arguments to be passed to command
                )
            )
        # end button creation for loop

        # Place the buttons
        for i in range(4):
            x = -1  # init temporary position variables
            y = -1
            if i % 2 == 1: # x values
                x = 0.25
            else:
                x = 0.75
            
            if i < 2: # y values
                y = 0.58
            else:
                y = 0.85

            buttons[i].place(relx=x, rely=y, relwidth=0.4, relheight=.25, anchor=tk.CENTER)
        # end button placement for loop

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="Back", font=backbuttonfont,
            width=100, height=50, command=back_function
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
