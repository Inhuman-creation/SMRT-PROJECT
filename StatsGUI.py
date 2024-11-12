# =====================
# StatsGUI.py
# Latest version: Nov 11
# Interactive graph and statistics GUI
# =====================

import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class StatsGUI:
    """
    This class contains the GUI for User progress and statistics
    """
    def __init__(self, controller):
        self.x_slider = None
        self.feedback_label = None
        self.controller = controller
        self.app = controller.app

        # Create frame for the GUI
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both", anchor=tk.CENTER)

        # Create fonts (all "Garet")
        flashfont = ctk.CTkFont(family="Garet", size=150, weight="bold")
        buttonfont = ctk.CTkFont(family="Garet", size=45, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        feedbackfont = ctk.CTkFont(family="Garet", size=50, weight="bold")

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # Initialize the interactive graph with correct font argument
        self.create_interactive_graph(feedbackfont)

    def create_interactive_graph(self, feedbackfont):
        # Create a figure and axis for the graph
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        # Define a sample function, e.g., a sine wave for user interaction
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, label="Sine Wave")
        ax.set_title("Interactive Graph")
        ax.set_xlabel("X-Axis")
        ax.set_ylabel("Y-Axis")
        ax.legend()

        # Add the matplotlib figure to tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add a slider to control the x-axis position
        self.x_slider = ctk.CTkSlider(master=self.frame, from_=0, to=10, command=self.update_feedback)
        self.x_slider.place(relx=0.5, rely=0.85, relwidth=0.6, anchor=tk.CENTER)

        # Display feedback based on the x position
        self.feedback_label = ctk.CTkLabel(master=self.frame, font=feedbackfont, text="Feedback will appear here")
        self.feedback_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def update_feedback(self, x_value):
        # Calculate corresponding y-value from the function
        y_value = np.sin(float(x_value))

        # Update feedback label with current x and y values
        self.feedback_label.configure(text=f"X: {x_value:.2f}, Y: {y_value:.2f}")

    def destroy(self):
        self.frame.destroy()
