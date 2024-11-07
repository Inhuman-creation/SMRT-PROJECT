# =====================
# MenuGUI.py
# Latest version: Nov 6
# Main menu selection screen
# =====================

import customtkinter as ctk
import tkinter as tk
import Settings as Settings

class MenuGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Configure main frame
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Fonts
        buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")  # Larger font for buttons
        titlefont = ctk.CTkFont(family="Garet", size=120, slant="italic")  # Larger font for Hello/Hola

        # Button functions
        def choice_function():
            self.controller.show_choice_gui()

        def text_function():
            self.controller.show_text_gui()

        def placeholder_function():
            print("Placeholder function")

        def exit_button():
            print("Exiting application")
            self.app.destroy()

        # Title with fade-in/fade-out animation for "Hello" and "Hola"
        self.title_label = ctk.CTkLabel(master=self.frame, text="Hello", text_color="black", font=titlefont)
        self.title_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)  # Adjusted to center the title
        self.toggle_text = True
        self.fade_title()

        # Create option buttons with specified colors and white text
        button_colors = ["#f37d59", "#0f606b", "#ffc24a"]
        button_texts = ["Multiple Choice Flashcards", "Text-Input Flashcards", "Statistics"]
        button_commands = [choice_function, text_function, placeholder_function]

        # Option buttons
        for i in range(3):
            button = ctk.CTkButton(
                master=self.frame, text=button_texts[i], font=buttonfont,
                fg_color=button_colors[i], text_color="#ffffff",  # White text
                width=900, height=80, command=button_commands[i], corner_radius=15
            )
            button.place(relx=0.5, rely=0.35 + (i * 0.2), anchor=tk.CENTER)

        # "EXIT" button at the bottom
        exit_btn = ctk.CTkButton(
            master=self.frame, text="EXIT", font=ctk.CTkFont(family="Garet", size=30, weight="bold"),
            width=120, height=60, fg_color="#ff4040", text_color="white",
            command=exit_button, corner_radius=15
        )
        exit_btn.place(relx=0.5, rely=0.95, anchor=tk.CENTER)  # Centered at bottom

    def fade_title(self):
        # Fade-in and fade-out between "Hello" and "Hola"
        current_text = self.title_label.cget("text")
        new_text = "Hola" if current_text == "Hello" else "Hello"
        self.title_label.configure(text=new_text)

        # Fade effect by adjusting opacity
        self.fade_in_out(0, new_text)  # Start the fade in

    def fade_in_out(self, alpha, new_text):
        # Gradually fade in and out by changing opacity (this simulates the fade)
        if alpha < 1:
            self.title_label.configure(text=new_text)
            self.frame.after(50, self.fade_in_out, alpha + 0.1, new_text)
        else:
            self.frame.after(3000, self.fade_title)  # Pause for 3 seconds before fading again

    def destroy(self):
        self.frame.destroy()
