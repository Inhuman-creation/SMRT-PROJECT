import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image, ImageTk

class AboutGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create frame for GUI with background color
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Fonts
        # Fonts
        titlefont = ctk.CTkFont(family="Garet", size=75, weight="bold")  # Title font
        backbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        cardfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        signaturefont = ctk.CTkFont(family="Brush Script MT", size=80, slant="italic", weight="normal")  # More signature-like font

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
        title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)  # Centered title near the top

        # Main text content label (slightly shorter rectangle on the left half of the screen)
        card = ctk.CTkLabel(
            master=self.frame,
            text=(
                "SMRT Vocab is the smarter way to learn a new language. Forget frustrating limits like health systems, "
                "rigid lessons, or boring topics. Our powerful algorithm focuses on the most essential vocabulary—the words "
                "you’ll actually use.\n\n"
                "By closing the 'vocabulary gap,' SMRT Vocab helps you go beyond the basics and gain the confidence to enjoy "
                "movies, books, and even conversations in your target language.\n\n"
                "No distractions. No limits. Just smarter learning. With SMRT Vocab, the world of language is yours to explore!"
            ),
            font=cardfont, text_color="white", fg_color="#acb87c", corner_radius=15,
            wraplength=650, anchor=tk.CENTER, justify=tk.LEFT
        )
        card.place(relx=0.35, rely=0.55, relwidth=0.6, relheight=0.7, anchor=tk.CENTER)

        # Check the current working directory to ensure file path is correct
        print("Current working directory:", os.getcwd())  # For debugging path

        # Load the logo image with transparency using PIL
        try:
            # Load image with transparency using PIL
            logo_image_pil = Image.open(os.path.join("assets", "SMRT_Vocab_logo.png"))

            # Resize the image to make it larger
            logo_image_pil = logo_image_pil.resize((600, 600))

            # Create CTkImage with the resized image (preserving transparency)
            logo_image = ctk.CTkImage(light_image=logo_image_pil, size=(400, 400))
            print("Logo loaded successfully!")
        except Exception as e:
            print(f"Error loading logo image: {e}")
            logo_image = None  # Fallback if the image doesn't load

        if logo_image:
            # Logo label (on the right half of the screen)
            logo_label = ctk.CTkLabel(
                master=self.frame,
                image=logo_image,
                text=""
            )
            logo_label.place(relx=0.83, rely=0.4, relwidth=0.3, relheight=0.6, anchor=tk.CENTER)

            lang_gang_label = ctk.CTkLabel(
                master=self.frame,
                text="- Lang Gang",
                font=signaturefont,
                text_color="black",
                fg_color="#fdf3dd"
            )
            lang_gang_label.place(relx=0.82, rely=0.74, anchor=tk.CENTER)

            # Store the reference to the logo image to prevent it from being garbage collected
            self.logo_image = logo_image
        else:
            print("Logo image not loaded successfully.")

        # Back button
        back_icon = ctk.CTkImage(light_image=Image.open("Assets/back-icon.png"), size=(30, 30))
        exit_button = ctk.CTkButton(
            master=self.frame, text="BACK", font=backbuttonfont,
            width=120, height=60, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=15,  # White text and red color
            image=back_icon, compound="left"
            )
        exit_button.place(relx=0.055, rely=0.06, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()

