# =====================
# LoginGUI.py
# Latest version: Nov 7
# Login screen
# =====================
import customtkinter as ctk
import tkinter as tk
import csv
from tkinter import *
import shutil
import Settings
from WalkingWindow import WalkingWindow
import os

class LoginGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create main frame for the login page
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Creating fonts
        headerfont = ctk.CTkFont(family="Garet", size=100)  # Larger font for "Login" label
        buttonfont = ctk.CTkFont(family="Garet", size=28, weight="bold")
        feedbackbuttonfont = ctk.CTkFont(family="Garet", size=18, weight="bold")
        entryfont = ctk.CTkFont(family="Garet", size=28)  # Unbolded for entries
        italicsfont = ctk.CTkFont(family="Garet", size=18, slant="italic")

        # Welcome messages in different languages
        self.welcome_messages = ["Welcome", "Bienvenido", "Bienvenue", "أهلا بك", "Willkommen", "Benvenuto", "欢迎", "Добро пожаловать"]
        self.current_welcome_index = 0

        # Welcome label
        self.welcome_label = ctk.CTkLabel(master=self.frame, text=self.welcome_messages[self.current_welcome_index], font=headerfont, text_color="black")
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
            feedback_text = feedback
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=feedback_text, font=feedbackbuttonfont, text_color="black",
                fg_color="grey75"
            )
            feedback_label.place(relx=0.5, rely=0.9, relwidth=0.3, relheight=0.2, anchor=tk.CENTER)

            def feedback_function():
                feedback_label.destroy()
                feedback_button.destroy()

            feedback_button = ctk.CTkButton(
                master=self.frame, text="OK", font=feedbackbuttonfont,
                width=160, height=100, command=feedback_function, fg_color="#000080"
            )
            feedback_button.place(relx=0.5, rely=0.75, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)

        # Button functions
        def login_function():
            username = self.text_entry_username.get()
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            if not username.strip() or not email.strip() or not password.strip():
                show_feedback("Please Complete All Fields")
                return

            # Check provided credentials
            login_success = False
            with open("AccountInformation.csv", mode="r") as accountsFile:
                reader = csv.DictReader(accountsFile)
                for row in reader:
                    if username == row["Username"] and password == row["Password"]:
                        login_success = True

            if not login_success:
                show_feedback("Incorrect Username and Password")
                return 

            # Get the user's last index from Windows.csv for WalkingWindow
            user_last = 0
            with open("Windows.csv", mode="r") as windows_file:
                reader = csv.DictReader(windows_file)
                for row in reader:
                    if row["Username"] == username:
                        user_last = int(row["Last"])

            # Make Username_Spanish.csv if necessary
            user_file_path = f"UserWords/{username}_Spanish.csv"
            if not os.path.exists(user_file_path):
                if not os.path.exists("UserWords/Template_Spanish.csv"):
                    show_feedback("ERROR: UserWords/Template_Spanish.csv NOT FOUND")
                    return
                shutil.copy("UserWords/Template_Spanish.csv", user_file_path)

            # init WalkingWindow
            self.controller.study_window = WalkingWindow(size=Settings.WALKING_WINDOW_SIZE)
            self.controller.study_window.read_from_csv(user_file_path, num_rows=Settings.WALKING_WINDOW_SIZE)
            self.controller.username = username

            self.controller.show_menu_gui()

        def signup_function():
            username = self.text_entry_username.get()
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            # Check that all field have something
            if not username.strip() or not email.strip() or not password.strip():
                show_feedback("Please Complete All Fields")
                return
            
            # Check username for unallowed characters (Windows file naming constraint)
            unallowed_characters = "<>:\"/\\|?*"
            for c in unallowed_characters:
                if c in username:
                    show_feedback("Do not use the following characters: \n<>:\"/\\|?*")
                    return
            
            # check if username already exists in the application
            with open("AccountInformation.csv", mode="r") as accounts_file:
                reader = csv.DictReader(accounts_file)
                for row in reader:
                    if row["Username"] == username:
                        show_feedback("That Username is Taken\nTry Another")
                        return

            account_data = {
                'Username': username,
                'Password': password,
                'Email': email
            }

            # Write account data to AccountInformation.csv
            with open('AccountInformation.csv', mode='a', newline='') as file:
                fieldnames = account_data.keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                file.seek(0, 2)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(account_data)
            
            # Initialize Windows.csv for this user
            with open("Windows.csv", mode="a") as windows_file:
                windows_file.write(f"{username},0\n")
            
            # copy UserWords/Template_Spanish.csv to UserWords/Username_Spanish.csv
            user_file_path = f"UserWords/{username}_Spanish.csv"
            if not os.path.exists("UserWords/Template_Spanish.csv"):
                show_feedback("ERROR: UserWords/Template_Spanish.csv NOT FOUND")
                return
            shutil.copy("UserWords/Template_Spanish.csv", user_file_path)

            # initialize walking window
            self.controller.study_window = WalkingWindow(size=Settings.WALKING_WINDOW_SIZE)
            self.controller.study_window.read_from_csv(user_file_path, num_rows=Settings.WALKING_WINDOW_SIZE)
            self.controller.username = username

            self.controller.show_menu_gui()

        def exit_button():
            self.app.destroy()

        # Main white rectangle frame for text inputs and buttons
        input_frame = ctk.CTkFrame(master=self.frame, fg_color="white", corner_radius=15)
        input_frame.place(relx=0.5, rely=0.6, relwidth=0.55, relheight=0.6, anchor=tk.CENTER)

        # Header label "Login"
        header_label = ctk.CTkLabel(master=input_frame, text="Login", font=ctk.CTkFont(family="Garet", size=35, weight="bold"), text_color="black")
        header_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        # Text entries
        self.text_entry_username = ctk.CTkEntry(
            master=input_frame, placeholder_text="Username", font=entryfont,
            fg_color="white", border_color="lightgray", border_width=2, text_color="black"
        )
        self.text_entry_username.place(relx=0.5, rely=0.2, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)

        self.text_entry_password = ctk.CTkEntry(
            master=input_frame, placeholder_text="Password", font=entryfont, show="*",
            fg_color="white", border_color="lightgray", border_width=2, text_color="black"
        )
        self.text_entry_password.place(relx=0.5, rely=0.35, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)

        self.text_entry_email = ctk.CTkEntry(
            master=input_frame, placeholder_text="Email", font=entryfont,
            fg_color="white", border_color="lightgray", border_width=2, text_color="black"
        )
        self.text_entry_email.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)

        # "Login" button above "Register your account"
        loginbutton = ctk.CTkButton(
            master=input_frame, text="Login", font=buttonfont, command=login_function,
            fg_color="#f37d59", text_color="white", corner_radius=10
        )
        loginbutton.place(relx=0.5, rely=0.7, relwidth=0.7, relheight=0.1, anchor=tk.CENTER)

        # Informative text above "Register your account" button
        register_text = ctk.CTkLabel(
            master=input_frame, text="Don't have an account? Click the button below.",
            font=italicsfont, text_color="black"
        )
        register_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # "Register your account" button
        signupbutton = ctk.CTkButton(
            master=input_frame, text="Register your account", font=buttonfont, command=signup_function,
            fg_color="#0f606b", text_color="white", corner_radius=10
        )
        signupbutton.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.1, anchor=tk.CENTER)

        # "EXIT" button at the bottom
        exit_btn = ctk.CTkButton(
            master=self.frame, text="EXIT", font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=120, height=60, fg_color="#ff4040", text_color="white",
            command=exit_button, corner_radius=15
        )
        exit_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  # Centered at bottom

    def destroy(self):
        self.frame.destroy()
