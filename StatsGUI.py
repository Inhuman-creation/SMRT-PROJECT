# =====================
# StatsGUI.py
# Latest version: Nov 11
# Interactive graph and statistics GUI
# =====================

#import csv
import customtkinter as ctk
import tkinter as tk

import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


def custom_function(x):
    y = 114.4083 + (-1.124367 - 114.4083)/(1 + (x/616.4689)**0.7302358)
    return max(0,y)
    #this function is an approximated curve fit based off linguistic sources and rounding.


def count_known_words(words_dict):
    totalknown =0
    for x in words_dict:
        if words_dict[x].is_known:
            totalknown += 1
    return totalknown

def determine_most_incorrect(words_dict):
    num_incorrect = 0
    most_incorrect = None
    for x in words_dict:
        if words_dict[x].count_incorrect > num_incorrect:
            most_incorrect = words_dict[x].foreign
            num_incorrect = words_dict[x].count_incorrect
    return most_incorrect

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
        self.x_slider = None
        self.feedback_label = None
        self.controller = controller
        self.app = controller.app
        self.default_x = count_known_words(self.controller.study_window.words_dict)
        #self.most_incorrect = determine_most_correct(self.controller.study_window.words_dict) #POSSIBLILITY TO INCLUDE
        self.most_incorrect = determine_most_incorrect(self.controller.study_window.words_dict)
        self.most_difficult = determine_most_difficult(self.controller.study_window.words_dict)


        # Create frame for the GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        # Create fonts (all "Garet")
        #flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        #buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        card = ctk.CTkLabel(
            master=self.frame, text="Total Known Words:\n" + str(self.default_x), text_color="white",
            font=backbuttonfont, fg_color="#acb87c", corner_radius=15 # from choice GUI
        )
        card.place(relx=0.5, rely=0.2, relwidth=.15, relheight=.1, anchor=tk.CENTER)

        stats_card = ctk.CTkLabel(
            master=self.frame,
            text="Hardest Word:\n" + str(self.most_difficult) +"\n\n Worst Word:\n"+ str(self.most_incorrect),
            text_color="white",
            font=backbuttonfont, fg_color="#0f606b", corner_radius=15  # from choice GUI
        )
        stats_card.place(relx=0.90, rely=0.5, relwidth=.15, relheight=.25, anchor=tk.CENTER)

        self.create_interactive_graph(feedbackfont)

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
        y = np.maximum(0, y) #does not allow negative y values.
        ax.plot(x, y, label="Language Knowledge Curve")
        #Graph the users progress through the language
        ax.axvline(count_known_words(self.controller.study_window.words_dict),
                    color='red', linestyle='-', label="You are here")
        ax.set_title("Check your progress")
        ax.set_xlabel("Number of Known Words")
        ax.set_ylabel("Percentage of Language Known")
        ax.legend()

        # Add the matplotlib figure to tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add a slider to control the x-axis position
        self.x_slider = ctk.CTkSlider(master=self.frame, from_=1, to=5000, command=self.update_feedback)
        self.x_slider.place(relx=0.5, rely=0.85, relwidth=0.6, anchor=tk.CENTER)

        # Display feedback based on the x position
        self.feedback_label = ctk.CTkLabel(master=self.frame, font=backbuttonfont, text="Slide to Compare!", text_color="black")
        self.feedback_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def update_feedback(self, x_value):
        # Calculate corresponding y-value from the function
        y_value = custom_function(int(x_value))
        # Update feedback label with current x and y values
        self.feedback_label.configure(text=f"{x_value:.0f} words ~ {y_value:.0f} Percent")

    def destroy(self):
        plt.close('all')
        self.frame.destroy()
