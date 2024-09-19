import customtkinter as ctk
#from customtkinter import CTk
import tkinter as tk
import ChoiceGUI

class Menu:
    def __init__(self):

        app = ctk.CTk()
        app.geometry("1000x1000")
        app._state_before_windows_set_titlebar_color = 'zoomed'
        app.title("SMRT")

        # sets default color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        #creates button font
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")

        # creates function for button to work
        def startButton():
            app.destroy()
            ChoiceGUI.MultipleChoiceGUI()
        def button_function2():
            print("hi")

        def button_function3():
            print("hi")

        def exit_Button():
            print("exit")
            exit(0)

        # creates buttons to navigate the menu

        start = ctk.CTkButton(master=app, text="Start", font=buttonfont, hover_color="green",
                                width=350, height=200, command=startButton)
        start.place(relx=0.5, rely=0.12,relwidth=.3,relheight=.2, anchor=tk.CENTER)

        # creates button number 2

        button2 = ctk.CTkButton(master=app, text="placeholder", font=buttonfont, hover_color="green",
                                width=350, height=200, command=button_function2)
        button2.place(relx=0.5, rely=0.35,relwidth=.3,relheight=.2, anchor=tk.CENTER)

        # creates button number 3

        button3 = ctk.CTkButton(master=app, text="placeholder", font=buttonfont, hover_color="green",
                                width=350, height=200, command=button_function3)
        button3.place(relx=0.5, rely=0.58,relwidth=.3,relheight=.2, anchor=tk.CENTER)

        # creates button number 4

        button4 = ctk.CTkButton(master=app, text="Exit", font=buttonfont, hover_color="green",
                                width=350, height=200, command=exit_Button)
        button4.place(relx=0.50, rely=0.81,relwidth=.3,relheight=.2, anchor=tk.CENTER)

        # prevents window from closing at the end of the code
        app.mainloop()
