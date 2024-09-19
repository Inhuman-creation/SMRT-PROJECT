import customtkinter as ctk
import tkinter as tk
import InitializationFunctions
from InitializationFunctions import variableinitialization

class MultipleChoiceGUI():
    def __init__(self):
        # creates variable to use for button 1 by calling a function from
        # Intialization function which returns a list.
        flashword, var1, var2, var3, var4 = variableinitialization()

        # creates main window
        app = ctk.CTk()
        app.geometry("1000x1000")
        app._state_before_windows_set_titlebar_color = 'zoomed'
        app.title("Menu")

        # creates function for button to work
        def button_function1():
            print(var1)

        def button_function2():
            print(var2)

        def button_function3():
            print(var3)

        def button_function4():
            var4 = "it works"
            button4.configure(text=var4)
            print(var4)

        def back_function():
            import MenuGUI
            app.destroy()
            MenuGUI.Menu()

        # creates font for flashcard
        flashfont = ctk.CTkFont(family="Times New Roman", size=75, weight="bold")
        # creates font for buttons
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")
        #creates back button font
        backbuttonfont = ctk.CTkFont(family="Times New Roman", size=25, weight="bold")
        # creates frame for flash car

        flashcard = ctk.CTkLabel(master=app, text=flashword, text_color="black",
                                 font=flashfont, bg_color="white",
                                 width=800, height=500,
                                 fg_color="grey75", corner_radius=0,
                                 )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)
        # sets appearance mode dark
        ctk.set_appearance_mode("Dark")

        # sets default color theme
        ctk.set_default_color_theme("blue")

        # creates a button for multiple choice selection

        button1 = ctk.CTkButton(master=app, text=var1, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function1)
        button1.place(relx=0.25, rely=0.58, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates button number 2

        button2 = ctk.CTkButton(master=app, text=var2, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function2)
        button2.place(relx=0.75, rely=0.58, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates button number 3

        button3 = ctk.CTkButton(master=app, text=var3, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function3)
        button3.place(relx=0.25, rely=0.85, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates button number 4

        button4 = ctk.CTkButton(master=app, text=var4, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function4)
        button4.place(relx=0.75, rely=0.85, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates back button
        backbutton = ctk.CTkButton(master=app, text="Back", font=backbuttonfont, hover_color="green",
                                   width=100, height=50, command=back_function)
        backbutton.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # prevents window from closing at the end of the code
        app.mainloop()



