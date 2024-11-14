

#import MenuGUI as MenuGUI
import customtkinter as ctk
import tkinter as tk

class AboutGUI:
    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create frame for  GUI with background color
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")

        # Button functions
        def back_function():
            self.controller.show_menu_gui()

        card = ctk.CTkLabel(
            master=self.frame,
            text=
                "SMRT Vocab is a vocabulary trainer designed to accelerate the acquisition of foreign languages.\n\n"
                "Unlike other applications, SMRT Vocab doesn't slow your progress with artificial constraints like health systems, "
                "rigid learning paths, or \nrestrictive topics. Our algorithm helps you learn the most common—and most essential—vocabulary quickly. "
                "We believe that addressing \nthe 'vocabulary gap' is the best way to move you beyond basic comprehension, opening the door to enjoyable lang activities.\n\n"
                "With SMRT Vocab, we hope you'll soon find yourself ready for exciting new experiences like listening to podcasts, watching movies,\n reading books, and, "
                "most importantly, speaking with others in your target lang.\n\n - Lang Gang",

            font=backbuttonfont, text_color="white", fg_color="#acb87c", corner_radius=15, wraplength=2000,
            anchor=tk.W, justify=tk.LEFT
        )
        card.place(relx=0.5, rely=0.5, relwidth=.875, relheight=.80, anchor=tk.CENTER)

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20  # from Choice GUI
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

    def destroy(self):
        self.frame.destroy()