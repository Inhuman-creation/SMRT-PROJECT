# =====================
# LoginGUI.py
# Latest version: Nov 7
# Login screen
# =====================

import customtkinter as ctk
import tkinter as tk
import csv
from tkinter import *

class LoginGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create main frame for the login page
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Creating fonts
        headerfont = ctk.CTkFont(family="Garet", size=100)
        buttonfont = ctk.CTkFont(family="Garet", size=28, weight="bold")
        feedbackbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        entryfont = ctk.CTkFont(family="Garet", size=28)
        italicsfont = ctk.CTkFont(family="Garet", size=18, slant="italic")

        # Welcome messages
        self.welcome_messages = ["Welcome", "Bienvenido", "Bienvenue", "أهلا بك", "Willkommen", "Benvenuto", "欢迎", "Добро пожаловать"]
        self.current_welcome_index = 0

        # Welcome label
        self.welcome_label = ctk.CTkLabel(master=self.frame, text=self.welcome_messages[self.current_welcome_index], font=headerfont, text_color="black")
        self.welcome_label.place(relx=0.5, rely=0.18, anchor=tk.CENTER)

        def switch_welcome_message():
            self.current_welcome_index = (self.current_welcome_index + 1) % len(self.welcome_messages)
            self.welcome_label.configure(text=self.welcome_messages[self.current_welcome_index])
            self.app.after(2000, switch_welcome_message)
        switch_welcome_message()

        # Button functions
        def login_function():
            username = self.text_entry_username.get()
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            if not username.strip() or not email.strip() or not password.strip():
                display_feedback("Please fill out all fields!", "#ffc24a", "white")
                return
            feedback_text = f"Username entered: {username}"
            display_feedback(feedback_text, "grey75", "black")
            if username.strip() and password.strip() and email.strip():
                self.controller.show_menu_gui()

        def signup_function():
            username = self.text_entry_username.get()
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            if not username.strip() or not email.strip() or not password.strip():
                display_feedback("Please fill out all fields!", "#ffc24a", "white")
                return

            account_data = {'Username': username, 'Password': password, 'Email': email}
            with open('AccountInformation.csv', mode='a', newline='') as file:
                fieldnames = account_data.keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                file.seek(0, 2)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(account_data)

            if username.strip() and password.strip() and email.strip():
                self.controller.show_menu_gui()

        def display_feedback(text, bg_color, text_color):
            feedback_label = ctk.CTkLabel(
                master=self.frame, text=text, font=feedbackbuttonfont,
                text_color=text_color, fg_color=bg_color, corner_radius=15
            )
            feedback_label.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.12, anchor=tk.CENTER)

            def feedback_function():
                feedback_label.destroy()
                feedback_button.destroy()

            feedback_button = ctk.CTkButton(
                master=self.frame, text="OK", font=feedbackbuttonfont,
                width=120, height=40, command=feedback_function,
                fg_color="#acb87c", corner_radius=10, text_color="white"
            )
            feedback_button.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

        def exit_button():
            self.app.destroy()

        # Main input frame and UI elements setup (input_frame, buttons, labels)
        input_frame = ctk.CTkFrame(master=self.frame, fg_color="white", corner_radius=15)
        input_frame.place(relx=0.5, rely=0.6, relwidth=0.55, relheight=0.6, anchor=tk.CENTER)
        header_label = ctk.CTkLabel(master=input_frame, text="Login", font=ctk.CTkFont(family="Garet", size=35, weight="bold"), text_color="black")
        header_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        self.text_entry_username = ctk.CTkEntry(master=input_frame, placeholder_text="Username", font=entryfont, fg_color="white", border_color="lightgray", border_width=2, text_color="black")
        self.text_entry_username.place(relx=0.5, rely=0.2, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)
        self.text_entry_password = ctk.CTkEntry(master=input_frame, placeholder_text="Password", font=entryfont, show="*", fg_color="white", border_color="lightgray", border_width=2, text_color="black")
        self.text_entry_password.place(relx=0.5, rely=0.35, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)
        self.text_entry_email = ctk.CTkEntry(master=input_frame, placeholder_text="Email", font=entryfont, fg_color="white", border_color="lightgray", border_width=2, text_color="black")
        self.text_entry_email.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.08, anchor=tk.CENTER)
        loginbutton = ctk.CTkButton(master=input_frame, text="Login", font=buttonfont, command=login_function, fg_color="#f37d59", text_color="white", corner_radius=10)
        loginbutton.place(relx=0.5, rely=0.7, relwidth=0.7, relheight=0.1, anchor=tk.CENTER)
        register_text = ctk.CTkLabel(master=input_frame, text="Don't have an account? Click the button below.", font=italicsfont, text_color="black")
        register_text.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        signupbutton = ctk.CTkButton(master=input_frame, text="Register your account", font=buttonfont, command=signup_function, fg_color="#0f606b", text_color="white", corner_radius=10)
        signupbutton.place(relx=0.5, rely=0.9, relwidth=0.7, relheight=0.1, anchor=tk.CENTER)
        exit_btn = ctk.CTkButton(master=self.frame, text="EXIT", font=ctk.CTkFont(family="Garet", size=30, weight="bold"), width=120, height=60, fg_color="#ff4040", text_color="white", command=exit_button, corner_radius=15)
        exit_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()
