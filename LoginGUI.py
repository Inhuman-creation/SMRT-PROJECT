import customtkinter as ctk
import tkinter as tk
import csv
from tkinter import *
import time

class LoginGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Creation of the main frame for the login page (using customtkinter)
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
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


            #Read login information to dictionary and reference for verifing login information
            #####
            '''def csv_to_dict_and_back(file_path):

                # Read the CSV contents into a dictionary
                data_dict = {}
                #with open(AccountInformation.csv, mode='r') as csv_file:
                    #reader = csv.reader(csv_file)
                reader = csv.DictReader(open('AccountInformation.csv'))
                for row in reader:
                    if row:  # Check if row is not empty
                        Username = row[0]
                        Email = row[1]
                        Password = row[2]
                        data_dict[Username] = username

                for i in csv.DictReader('AccountInformation.csv'):
                    print(data_dict(i))

                # Write the dictionary back to the original file
                with open(file_path, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in data_dict.items():
                        writer.writerow([key] + value)

            # Replace 'yourfile.csv' with the path to your CSV file
            file_path = 'AccountInformation.csv'
            csv_to_dict_and_back(file_path)
            '''

            ###


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
            # Access the text entry values
            username = self.text_entry_username.get()
            password = self.text_entry_password.get()
            email = self.text_entry_email.get()

            # Popup label if login information needs correcting
            if not username.strip() or not email.strip() or not password.strip():  # Check if username is empty
                feedback_text = "Please Complete All Fields"

                #Feedback functionality had to be immplemented inside if statement so user would not be able to continue until
                #the information was corrected
                # Create or update feedback label
                feedback_label = ctk.CTkLabel(
                    master=self.frame, text=feedback_text, font=feedbackbuttonfont, text_color="black",
                    fg_color="grey75"
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
                return

            else:
                print("All fields are entered correctly.")
                feedback_text = "Username entered: {}".format(username)

                # Create or update feedback label
                feedback_label = ctk.CTkLabel(
                    master=self.frame, text=feedback_text, font=feedbackbuttonfont, text_color="black",
                    fg_color="grey75"
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


            # Create an empty dictionary and store user input
            account_data = {
                'Username': username,
                'Password': password,
                'Email': email
            }

            # Send dictionary information to be saved in AccountInformation.csv
            #Mode 'a' is for append as to not overwrite, since we are just adding a new account, not doing
            #anything with old ones
            with open('AccountInformation.csv', mode='a', newline='') as file:
                # Extract field names from the first dictionary
                fieldnames = account_data.keys()

                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write the header only if the file is new or empty
                file.seek(0, 2)  # Move the cursor to the end of the file
                if file.tell() == 0:  # Check if the file is empty
                    writer.writeheader()

                # Write the single dictionary row
                writer.writerow(account_data)

            # If username, password, and email are not empty, proceed with the next screen
            if username.strip() and password.strip() and email.strip():
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
