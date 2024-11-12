# =====================
# StatsGUI.py
# Latest version: Nov 11
# Interactive graph and statistics GUI
# =====================

#import csv
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from Word import Word
import Settings


def custom_function(x):
    return 114.4083 + (-1.124367 - 114.4083)/(1 + (x/616.4689)**0.7302358)
    #this function is an approximated curve fit based off linguistic sources and rounding.


def count_known_words(words_dict):
    totalknown =0
    for x in words_dict:
        if words_dict[x].is_known:
            totalknown += 1
    return totalknown


class StatsGUI:
    """
    This class contains the GUI for User progress and statistics
    """
    def __init__(self, controller):
        self.x_slider = None
        self.feedback_label = None
        self.controller = controller
        self.app = controller.app
        self.default_x = count_known_words(self.controller.study_window.words_dict)


        # Create frame for the GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        # Create fonts (all "Garet")
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        #buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        # Initialize the interactive graph
        card = ctk.CTkLabel(
            master=self.frame, text="Total Known Words:\n" + str(self.default_x), text_color="black",
            font=backbuttonfont, fg_color=None  # from choice GUI
        )
        card.place(relx=0.5, rely=0.1, relwidth=.2, relheight=.3, anchor=tk.CENTER)
        print("Flashcard created!")

        self.create_interactive_graph(feedbackfont)
        print("Graph created!")

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def create_interactive_graph(self, backbuttonfont):
        # Create a figure and axis for the graph
        fig, ax = plt.subplots(figsize=(10, 4), dpi=100)

        # Define a sample function, e.g., a sine wave for user interaction
        x = np.linspace(0, 5000, 100)
        y = 114.4083 + (-1.124367 - 114.4083)/(1 + (x/616.4689)**0.7302358)
        ax.plot(x, y, label="Line")
        ax.set_title("Check your progress")
        ax.set_xlabel("~ number of known words")
        ax.set_ylabel("~ percentage of language")
        ax.legend()

        # Add the matplotlib figure to tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add a slider to control the x-axis position
        self.x_slider = ctk.CTkSlider(master=self.frame, from_=0, to=5000, command=self.update_feedback)
        self.x_slider.place(relx=0.5, rely=0.85, relwidth=0.6, anchor=tk.CENTER)

        # Display feedback based on the x position
        self.feedback_label = ctk.CTkLabel(master=self.frame, font=backbuttonfont, text="Feedback will appear here", text_color="black")
        self.feedback_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def update_feedback(self, x_value):
        # Calculate corresponding y-value from the function
        y_value = custom_function(float(x_value))
        # Update feedback label with current x and y values
        self.feedback_label.configure(text=f"X: {x_value:.2f}, Y: {y_value:.2f}")

    def destroy(self):
        self.frame.destroy()
