import customtkinter as ctk
import tkinter as tk
import csv
from tkinter import *

class LoginGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Creation of the main frame for the login page (using customtkinter)
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000)
        self.frame.pack(expand=1, fill="both")

        # Create button font
        buttonfont = ctk.CTkFont(family="Garet", size=55, weight="bold")
        feedbackbuttonfont = ctk.CTkFont(family="Garet", size=20, weight="bold")

        # Button functions
        def login_function():
            # Access the text entry values
            username = self.text_entry_username.get()
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

        # Popup label if login information needs correcting
            if not username.strip() or not email.strip() or not password.strip():  # Check if username is empty
                feedback_text = "Please Complete All Fields"
            else:
                feedback_text = "Username entered: {}".format(username)


            # Create or update feedback label
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, font=feedbackbuttonfont, text_color="black", fg_color="grey75"
            )
            feedback_label.place(relx=0.5, rely=0.9, relwidth=0.3, relheight=0.2, anchor=tk.CENTER)

            def feedback_function():
                """This function is executed when the feedback/OK button is pressed to clear login feedback"""
                feedback_label.destroy()
                feedback_button.destroy()
                
            # Create a button to close the feedback
            feedback_button = ctk.CTkButton(
                master=self.frame, text="OK", font=buttonfont,
                width=160, height=100, command=feedback_function, fg_color="#000080"
            )
            feedback_button.place(relx=0.5, rely=0.75, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

            # If username is not empty, proceed with the next screen
            if username.strip() and password.strip() and email.strip():
                self.controller.show_menu_gui()

        def signup_function():
            self.controller.show_menu_gui()

        def exit_button():
            print("Exiting application")
            self.app.destroy()

        # Create frame to hold text input fields
        input_frame = ctk.CTkFrame(master=self.frame)
        input_frame.place(relx=0.5, rely=0.45, relwidth=0.5, relheight=0.4, anchor=tk.CENTER)

        # Create and place the text entry for username
        self.text_entry_username = ctk.CTkEntry(
            master=input_frame,
            placeholder_text="User Name",
            font=buttonfont
        )
        self.text_entry_username.place(relx=0.5, rely=0.20, relwidth=0.8, relheight=0.15, anchor=tk.CENTER)

        # Create and place the text entry for password (with masking)
        self.text_entry_password = ctk.CTkEntry(
            master=input_frame,
            placeholder_text="Password",
            font=buttonfont,
            show="*"  # Mask the password input
        )
        self.text_entry_password.place(relx=0.5, rely=0.45, relwidth=0.8, relheight=0.15, anchor=tk.CENTER)

        # Create and place the text entry for email
        self.text_entry_email = ctk.CTkEntry(
            master=input_frame,
            placeholder_text="Email",
            font=buttonfont
        )
        self.text_entry_email.place(relx=0.5, rely=0.70, relwidth=0.8, relheight=0.15, anchor=tk.CENTER)

        # Create buttons
        loginbutton = ctk.CTkButton(
            master=self.frame, text="Login", font=buttonfont,
            width=350, height=200, command=login_function
        )
        loginbutton.place(relx=0.35, rely=0.75, relwidth=.2, relheight=.1, anchor=tk.CENTER)

        signupbutton = ctk.CTkButton(
            master=self.frame, text="Signup", font=buttonfont,
            width=350, height=200, command=signup_function
        )
        signupbutton.place(relx=0.65, rely=0.75, relwidth=.2, relheight=.1, anchor=tk.CENTER)

        exit_btn = ctk.CTkButton(
            master=self.frame, text="Exit", font=buttonfont,
            width=350, height=200, command=exit_button
        )
        exit_btn.place(relx=0.5, rely=0.90, relwidth=.2, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
