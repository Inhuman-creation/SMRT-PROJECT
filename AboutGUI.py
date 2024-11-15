import customtkinter as ctk
import tkinter as tk
from tkinter import PhotoImage
import os

class AboutGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create frame for GUI with background color
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Fonts
        titlefont = ctk.CTkFont(family="Garet", size=75, weight="bold")  # Title font
        backbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        cardfont = ctk.CTkFont(family="Garet", size=18)

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        # "About Us" title label
        title_label = ctk.CTkLabel(
            master=self.frame,
            text="About Us",
            font=titlefont,
            text_color="black"
        )
        title_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)  # Centered title at the top

        # Main text content label (on the left half of the screen)
        card = ctk.CTkLabel(
            master=self.frame,
            text=(
                "SMRT Vocab is a vocabulary trainer designed to accelerate the acquisition of foreign languages. "
                "Unlike other applications, SMRT Vocab doesn't slow your progress with artificial constraints like health systems, "
                "rigid learning paths, or restrictive topics. Our algorithm helps you learn the most common—and most essential—vocabulary quickly. "
                "We believe that addressing the 'vocabulary gap' is the best way to move you beyond basic comprehension, opening the door to enjoyable language activities. "
                "With SMRT Vocab, we hope you'll soon find yourself ready for exciting new experiences like listening to podcasts, watching movies, "
                "reading books, and, most importantly, speaking with others in your target language. - Lang Gang"
            ),
            font=cardfont, text_color="white", fg_color="#acb87c", corner_radius=15,
            wraplength=850, anchor=tk.CENTER, justify=tk.LEFT
        )
        card.place(relx=0.25, rely=0.5, relwidth=0.45, relheight=0.7, anchor=tk.CENTER)  # Left half for content

        # Check the current working directory to ensure file path is correct
        print("Current working directory:", os.getcwd())  # For debugging path

        # Load the logo image (ensure the file path is correct)
        try:
            logo_image = PhotoImage(file="SMRT_Vocab_logo.png")  # Ensure the logo file is in the correct path
            print("Logo loaded successfully!")
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_image = None  # Fallback if the image doesn't load

        if logo_image:
            # Logo label (on the right half of the screen)
            logo_label = ctk.CTkLabel(
                master=self.frame,
                image=logo_image
            )
            logo_label.place(relx=0.75, rely=0.5, relwidth=0.45, relheight=0.7, anchor=tk.CENTER)  # Right half for logo

            # Store the reference to the logo image to prevent it from being garbage collected
            self.logo_image = logo_image
        else:
            print("Logo image not loaded successfully.")

        # Create back button with larger font
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=120, height=60, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.1, anchor=tk.CENTER)  # Back button in top left corner

    def destroy(self):
        self.frame.destroy()
