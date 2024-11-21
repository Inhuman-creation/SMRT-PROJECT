"""
StatsGUI.py
================
This is the GUI for the Statistics page.
The user is able to see their personalized
progress report for various aspects
of their learning.

Version: 3.0
Since: 11-16-2024
"""

import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# This function is an approximated curve fit based off linguistic sources and rounding.
def custom_function(x):
    y = 114.4083 + (-1.124367 - 114.4083)/(1 + (x/616.4689)**0.7302358)
    return max(0,y)

# Counts the total known words by the user
def count_known_words(words_dict):
    totalknown =0
    for x in words_dict:
        if words_dict[x].is_known:
            totalknown += 1
    return totalknown

# Calculates which word the user gets incorrect the most
def determine_most_incorrect(words_dict):
    num_incorrect = 0
    most_incorrect = None
    for x in words_dict:
        if words_dict[x].count_incorrect > num_incorrect:
            most_incorrect = words_dict[x].foreign
            num_incorrect = words_dict[x].count_incorrect
    return most_incorrect

# Calculates which word the user sees the most (struggles to learn)
def determine_most_difficult(words_dict):
    num_seen = 0
    most_seen = None
    for x in words_dict:
        if words_dict[x].count_seen > num_seen:
            most_seen = words_dict[x].foreign
            num_seen = words_dict[x].count_seen
    return most_seen

class StatsGUI:
    """
    This class contains the GUI for User progress and statistics
    """
    def __init__(self, controller):
        self.canvas = None
        self.x_value = None
        self.dynamic_line = None
        self.x_slider = None
        self.feedback_label = None
        self.controller = controller
        self.app = controller.app
        self.default_x = count_known_words(self.controller.study_window.words_dict)
        self.most_incorrect = determine_most_incorrect(self.controller.study_window.words_dict)
        self.most_difficult = determine_most_difficult(self.controller.study_window.words_dict)

        # Create frame for the GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        # Create fonts (all "Garet")
        backbuttonfont = ctk.CTkFont(family="Garet", size=30, weight="bold")
        knownwordsfont = ctk.CTkFont(family="Garet", size=60, weight="bold")
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        # Back button function
        def back_function():
            self.controller.show_menu_gui()

        # Known Words card
        card = ctk.CTkLabel(
            master=self.frame,
            text="Total Known Words: " + str(self.default_x),
            text_color="white",
            font=knownwordsfont,
            fg_color="#acb87c",
            corner_radius=15
        )
        card.place(relx=0.5, rely=0.2, relwidth=.8, relheight=.15, anchor=tk.CENTER)

        # Information on the user's words (most seen and worst word)
        stats_card = ctk.CTkLabel(
            master=self.frame,
            text="Most Seen Word:\n" + str(self.most_difficult) +"\n\n Worst Word:\n"+ str(self.most_incorrect),
            text_color="white",
            font=backbuttonfont,
            fg_color="#0f606b",
            corner_radius=15
        )
        stats_card.place(relx=0.86, rely=0.5, relwidth=.22, relheight=.25, anchor=tk.CENTER)

        # Load the logo image with transparency using PIL
        try:
            # Load image with transparency using PIL
            logo_image_pil = Image.open(os.path.join("assets", "SMRT_Vocab_logo.png"))

            # Resize the image to make it larger
            logo_image_pil = logo_image_pil.resize((600, 600))

            # Create CTkImage with the resized image (preserving transparency)
            logo_image = ctk.CTkImage(light_image=logo_image_pil, size=(200, 200))
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
            logo_label.place(relx=0.87, rely=0.8, relwidth=0.3, relheight=0.3, anchor=tk.CENTER)

            # Store the reference to the logo image to prevent it from being garbage collected
            self.logo_image = logo_image
        else:
            print("Logo image not loaded successfully.")

        self.create_interactive_graph(feedbackfont)

        # Back button
        back_icon = ctk.CTkImage(light_image=Image.open("Assets/back-icon.png"), size=(30, 30))
        exit_button = ctk.CTkButton(
            master=self.frame,
            text="BACK",
            font=backbuttonfont,
            width=120,
            height=60,
            command=back_function,
            fg_color="#d9534f",
            text_color="white",
            corner_radius=15,
            image=back_icon,
            compound="left"
        )
        exit_button.place(relx=0.055, rely=0.06, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    # Creat the graph
    def create_interactive_graph(self, backbuttonfont):
        # Create a figure and axis for the graph
        fig, ax = plt.subplots(figsize=(10, 4), dpi=100)

        # Define the function for the graph
        x = np.linspace(0, 5000, 100)
        y = 114.4083 + (-1.124367 - 114.4083)/(1 + (x/616.4689)**0.7302358)
        y = np.maximum(0, y) #does not allow negative y values.
        ax.plot(x, y, label="Language Knowledge Curve")
        #Graph the users progress through the language
        ax.axvline(count_known_words(self.controller.study_window.words_dict),
                    color='red', linestyle='--', label="You are here")
        self.dynamic_line, = ax.plot([self.default_x, self.default_x], [0, custom_function(self.default_x)],
                                     color="green", linestyle='-', label="Goal")
        ax.set_title("Check your progress")
        ax.set_xlabel("Number of Known Words")
        ax.set_ylabel("Percentage of Language Known")
        ax.legend()

        # Add the matplotlib figure to tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.38, rely=0.52, anchor=tk.CENTER)

        # Add a slider to see potential progress (what if calculator)
        self.x_slider = ctk.CTkSlider(
            master=self.frame,
            from_=1,
            to=5000,
            command=lambda value: self.update_feedback(value, canvas),
            fg_color="#dcdcdc",
            progress_color="#4682b4",
            button_color="#5f9ea0",
            button_hover_color="#4682b4"
        )
        self.x_slider.place(relx=0.38, rely=0.88, relwidth=0.6, anchor=tk.CENTER)

        # Display feedback based on the x position
        self.feedback_label = ctk.CTkLabel(master=self.frame, font=backbuttonfont, text="Slide to Compare!", text_color="black")
        self.feedback_label.place(relx=0.38, rely=0.8, anchor=tk.CENTER)

        self.x_slider.set(self.default_x)
        self.update_feedback(self.default_x, canvas)

    # Shows user how many words they need to know in order to reach a certain percentage of language acquisition
    def update_feedback(self, x_value, canvas=None):
        # Calculate corresponding y-value from the function
        y_value = custom_function(int(x_value))
        # Update feedback label with current x and y values
        self.feedback_label.configure(text=f"{x_value:.0f} words ~ {y_value:.0f} Percent")
        
        self.dynamic_line.set_xdata([x_value, x_value])
        self.dynamic_line.set_ydata([0,y_value])
        canvas.draw()

    def destroy(self):
        plt.close('all')
        self.frame.destroy()
