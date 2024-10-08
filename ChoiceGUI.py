# choiceGUI.py

import customtkinter as ctk
import tkinter as tk


class ChoiceGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Initialize variables for GUI display
        flashword, var1, var2, var3, var4 = self.controller.study_window.get_random_words(5)

        # Create frame for choice GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000)
        self.frame.pack(expand=1, fill="both")

        # Create fonts
        flashfont = ctk.CTkFont(family="Times New Roman", size=75, weight="bold")
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Times New Roman", size=25, weight="bold")

        # Button functions
        def button_function1():
            print(flashword.english)

        def button_function2():
            print(var2.english)

        def button_function3():
            print(var3.english)

        def button_function4():
            print(var4.english)

        def back_function():
            self.controller.show_menu_gui()

        # Create flashcard label
        flashcard = ctk.CTkLabel(
            master=self.frame, text=flashword.spanish, text_color="black",
            font=flashfont, fg_color="grey75"
        )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)

        # Create multiple choice buttons
        button1 = ctk.CTkButton(
            master=self.frame, text=flashword.english, font=buttonfont,
            width=480, height=250, command=button_function1
        )
        button1.place(relx=0.25, rely=0.58, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        button2 = ctk.CTkButton(
            master=self.frame, text=var2.english, font=buttonfont,
            width=480, height=250, command=button_function2
        )
        button2.place(relx=0.75, rely=0.58, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        button3 = ctk.CTkButton(
            master=self.frame, text=var3.english, font=buttonfont,
            width=480, height=250, command=button_function3
        )
        button3.place(relx=0.25, rely=0.85, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        button4 = ctk.CTkButton(
            master=self.frame, text=var4.english, font=buttonfont,
            width=480, height=250, command=button_function4
        )
        button4.place(relx=0.75, rely=0.85, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="Back", font=backbuttonfont,
            width=100, height=50, command=back_function
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
