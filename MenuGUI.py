import customtkinter as ctk
import tkinter as tk
import ChoiceGUI
from ChoiceGUI import MultipleChoiceGUI


def menuGUI():

    app2 = ctk.CTk()
    app2.geometry('1000x1000')
    app2.title("Menu")


    # sets default color theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")


    #creates button font
    buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")

    # creates function for button to work
    def startButton():
        app2.destroy()
        MultipleChoiceGUI()
    def button_function2():
        print("hi")

    def button_function3():
        print("hi")

    def exit_Button():
        print("exit")

    # creates buttons to navigate the menu

    start = ctk.CTkButton(master=app2, text="Start", font=buttonfont, hover_color="green",
                                width=350, height=200, command=startButton)
    start.place(relx=0.5, rely=0.12, anchor=tk.CENTER)

    # creates button number 2

    button2 = ctk.CTkButton(master=app2, text="placeholder", font=buttonfont, hover_color="green",
                                width=350, height=200, command=button_function2)
    button2.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    # creates button number 3

    button3 = ctk.CTkButton(master=app2, text="placeholder", font=buttonfont, hover_color="green",
                                width=350, height=200, command=button_function3)
    button3.place(relx=0.5, rely=0.58, anchor=tk.CENTER)

    # creates button number 4

    button4 = ctk.CTkButton(master=app2, text="Exit", font=buttonfont, hover_color="green",
                                width=350, height=200, command=exit_Button)
    button4.place(relx=0.50, rely=0.81, anchor=tk.CENTER)

    # prevents window from closing at the end of the code
    app2.mainloop()
