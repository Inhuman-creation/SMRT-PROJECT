"""
LoginGUI.py
================
This is the GUI for the Login screen. The
user will be prompted to enter their
email and password. If they do not have
an account, they will be prompted to register.

Version: 4.0
Since: 11-17-2024
"""
import customtkinter as ctk
import tkinter as tk
import csv
from tkinter import *
import shutil
import Settings
from WalkingWindow import WalkingWindow
import os
from PIL import Image
from functools import partial


class LoginGUI:
    """
    This class contains the GUI for the Login page.
    """
    def __init__(self, controller):
        """
        Initializes the GUI and sets up the layout and interactive elements.
        """
        self.controller = controller
        self.app = controller.app

        # Create main frame for the login page
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Creating fonts
        headerfont = ctk.CTkFont(family="Garet", size=100)  # Larger font for "Login" label
        buttonfont = ctk.CTkFont(family="Garet", size=28, weight="bold")
        feedbackbuttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        entryfont = ctk.CTkFont(family="Garet", size=28)  # Unbolded for entries
        italicsfont = ctk.CTkFont(family="Garet", size=18, slant="italic")

        # Welcome messages in different languages
        self.welcome_messages = ["Welcome", "Bienvenido", "Bienvenue", "أهلا بك", "Willkommen", "Benvenuto", "欢迎",
                                 "Добро пожаловать", "Hoş geldin"]
        self.current_welcome_index = 0

        # Welcome label
        self.welcome_label = ctk.CTkLabel(master=self.frame, text=self.welcome_messages[self.current_welcome_index],
                                          font=headerfont, text_color="black")
        self.welcome_label.place(relx=0.5, rely=0.18, anchor=tk.CENTER)

        # Function to switch the welcome message every 2 seconds
        def switch_welcome_message():
            if self.welcome_label.winfo_exists():
                self.current_welcome_index = (self.current_welcome_index + 1) % len(self.welcome_messages)
                self.welcome_label.configure(text=self.welcome_messages[self.current_welcome_index])
                self.app.after(2000, switch_welcome_message)

        # Start switching welcome messages
        switch_welcome_message()

        def show_feedback(feedback: str):
            """
            Provides feedback to the user depending on if they need to take action,
            or if their account was successfully registered.
            """
            feedback_text = feedback
            feedback_label = ctk.CTkLabel(
                master=self.frame,
                text=feedback_text,
                font=feedbackbuttonfont,
                text_color="white",
                fg_color="#f37d59",
                corner_radius=5
            )
            feedback_label.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.15, anchor=tk.CENTER)

            def feedback_function():
                feedback_label.destroy()
                feedback_button.destroy()

            # OK button for pop-ups
            feedback_button = ctk.CTkButton(
                master=self.frame,
                text="OK",
                font=feedbackbuttonfont,
                width=160,
                height=100,
                fg_color="#d9534f",
                text_color="white",
                corner_radius=5,
                command = feedback_function
            )
            feedback_button.place(relx=0.5, rely=0.7, relwidth=0.1, relheight=0.08,
                                  anchor=tk.CENTER)
            
        def registration_succ():
            """
            Provides feedback to the user depending on if they need to take action,
            or if their account was successfully registered.
            """
            feedback_text = "Registration Successful!"
            feedback_label = ctk.CTkLabel(
                master=self.frame,
                text=feedback_text,
                font=feedbackbuttonfont,
                text_color="white",
                fg_color="#77721f",
                corner_radius=5
            )
            feedback_label.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.15, anchor=tk.CENTER)

        # Button functions
        def login_function():
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            if not email.strip() or not password.strip():
                show_feedback("Please complete all fields!")
                return

            # Check provided credentials
            login_success = False
            with open("AccountInformation.csv", mode="r") as accountsFile:
                reader = csv.DictReader(accountsFile)
                for row in reader:
                    # If credentials are correct
                    if email == row["Email"] and password == row["Password"]:
                        login_success = True

            # If credentials are not correct
            if not login_success:
                show_feedback("Incorrect email or password!")
                return

            # Create user_lang.csv files if necessary
            for lang in Settings.LANGUAGE_OPTIONS:
                user_file_path = f"UserWords/{email}_{lang}.csv"
                if not os.path.exists(user_file_path):
                    if not os.path.exists(f"UserWords/Template_{lang}.csv"):
                        show_feedback(f"ERROR: UserWords/Template_{lang}.csv NOT FOUND")
                        return
                    shutil.copy(f"UserWords/Template_{lang}.csv", user_file_path)

            # init WalkingWindow
            Settings.username = email
            self.controller.study_window = WalkingWindow(size=Settings.WALKING_WINDOW_SIZE)
            self.app.protocol("WM_DELETE_WINDOW", self.controller.save_and_close)

            self.controller.show_menu_gui()

        def signup_function():
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            # Check that all field have something
            if not email.strip() or not password.strip():
                show_feedback("Please complete all fields!")
                return

            # Check email for not allowed characters (Windows file naming constraint)
            unallowed_characters = "<>:\"/\\|?*"
            for c in unallowed_characters:
                if c in email:
                    show_feedback("Emails should not contain the\n following characters: \n<>:\"/\\|?*")
                    return

            # Check if email already exists in the application
            with open("AccountInformation.csv", mode="r") as accounts_file:
                reader = csv.DictReader(accounts_file)
                for row in reader:
                    if row["Email"] == email:
                        show_feedback("That email is already in use!\n Register "
                                      "with another email.")
                        return

            account_data = {
                'Email': email,
                'Password': password
            }

            # Write account data to AccountInformation.csv
            with open('AccountInformation.csv', mode='a', newline='') as file:
                fieldnames = account_data.keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                file.seek(0, 2)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(account_data)

            # Copy Template_lang.csv files to user_lang.csv
            for lang in Settings.LANGUAGE_OPTIONS:
                user_file_path = f"UserWords/{email}_{lang}.csv"
                if not os.path.exists(f"UserWords/Template_{lang}.csv"):
                    show_feedback(f"ERROR: UserWords/Template_{lang}.csv NOT FOUND")
                    return
                shutil.copy(f"UserWords/Template_{lang}.csv", user_file_path)

            # Initialize walking window
            Settings.username = email
            self.controller.study_window = WalkingWindow(size=Settings.WALKING_WINDOW_SIZE)
            self.app.protocol("WM_DELETE_WINDOW", self.controller.save_and_close)

            # Display to the user that their registration was successful
            registration_succ() 
            self.frame.after(1000, self.controller.show_menu_gui)

        def exit_button():
            self.app.destroy()

        # Main white rectangle frame for text inputs and buttons
        input_frame = ctk.CTkFrame(master=self.frame,
                                   fg_color="white",
                                   corner_radius=15)
        input_frame.place(relx=0.5, rely=0.575, relwidth=0.55, relheight=0.625, anchor=tk.CENTER)

        # Header label "Welcome to SMRT Vocab"
        header_label = ctk.CTkLabel(master=input_frame,
                                    text="Welcome to SMRT Vocab",
                                    font=ctk.CTkFont(family="Garet", size=35, weight="bold"), text_color="black")
        header_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        # Load the logo image
        logo_image = ctk.CTkImage(light_image=Image.open("Assets/SMRT_Vocab_logo.png"),
                                  size=(140, 140))
        logo_label = ctk.CTkLabel(master=input_frame, image=logo_image, text="")
        logo_label.place(relx=0.5, rely=0.22, anchor=tk.CENTER)

        # Store the reference to prevent garbage collection
        self.logo_image = logo_image

        # Text fields

        # Email text field
        self.text_entry_email = ctk.CTkEntry(
            master=input_frame,
            placeholder_text="Email",
            font=entryfont,
            fg_color="white",
            border_color="lightgray",
            border_width=2,
            text_color="black"
        )
        self.text_entry_email.place(relx=0.5, rely=0.425, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)

        # Password text fields
        self.text_entry_password = ctk.CTkEntry(
            master=input_frame,
            placeholder_text="Password",
            font=entryfont,
            show="*",
            fg_color="white",
            border_color="lightgray",
            border_width=2,
            text_color="black"
        )
        self.text_entry_password.place(relx=0.5, rely=0.56, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)

        # "Login" button
        login_icon = ctk.CTkImage(light_image=Image.open("Assets/enter-icon.png"), size=(40, 40))
        loginbutton = ctk.CTkButton(
            master=input_frame,
            text="Login",
            font=buttonfont,
            command=login_function,
            fg_color="#acb87c",
            text_color="white",
            corner_radius=10,
            image=login_icon,
            compound="left"
        )
        loginbutton.place(relx=0.5, rely=0.7, relwidth=0.7, relheight=0.1, anchor=tk.CENTER)

        # Informative text above "Register your account" button
        register_text = ctk.CTkLabel(
            master=input_frame,
            text="Don't have an account? Click the button below.",
            font=italicsfont,
            text_color="black"
        )
        register_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # "Register your account" button
        register_icon = ctk.CTkImage(light_image=Image.open("Assets/register-icon.png"), size=(40, 40))
        signupbutton = ctk.CTkButton(
            master=input_frame,
            text="Register your account",
            font=buttonfont,
            command=signup_function,
            fg_color="#0f606b",
            text_color="white",
            corner_radius=10,
            image=register_icon,
            compound="left"
        )
        signupbutton.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.1, anchor=tk.CENTER)

        # "EXIT" button at the bottom
        exit_icon = ctk.CTkImage(light_image=Image.open("Assets/exit-icon.png"), size=(40, 40))
        exit_btn = ctk.CTkButton(
            master=self.frame,
            text="EXIT",
            font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=120,
            height=60,
            fg_color="#d9534f",
            text_color="white",
            command=exit_button,
            corner_radius=15,
            image=exit_icon,
            compound="left"
        )
        exit_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  # Centered at bottom

    def destroy(self):
        self.frame.destroy()