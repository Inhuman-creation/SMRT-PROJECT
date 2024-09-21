import customtkinter as ctk
#from customtkinter import CTk
import tkinter as tk


class GUI:
    def __init__(self):

        app = ctk.CTk()
        app.geometry("1000x1000")
        app._state_before_windows_set_titlebar_color = 'zoomed'
        app.title("SMRT")

        # sets default color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

    #INITIALIZES CHOICE GUI VARIABLES
    def variableinitialization(self):
        flashword = "por que"
        string1 = "word1"
        string2 = "word2"
        string3 = "word3"
        string4 = "word4"
        definition = "definition"

        return [flashword, string1, string2, string3, string4, definition]

    def menuGUI(self):
        frame = ctk.CTkFrame(master=None,height=1000,width=1000)
        frame._state_before_windows_set_titlebar_color = 'zoomed'
        frame.pack(expand=1,fill="both")

        # creates button font
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")

        # creates function for button to work
        def startButton():
            frame.destroy()
            GUI.choiceGUI(self)

        def button_function2():
            print("hi")

        def button_function3():
            print("hi")

        def exit_Button():
            print("exit")
            exit(0)

        # creates buttons to navigate the menu

        start = ctk.CTkButton(master=frame, text="Start", font=buttonfont, hover_color="green",
                              width=350, height=200, command=startButton)
        start.place(relx=0.5, rely=0.12, relwidth=.3, relheight=.2, anchor=tk.CENTER)

        # creates button number 2

        button2 = ctk.CTkButton(master=frame, text="placeholder", font=buttonfont, hover_color="green",
                                width=350, height=200, command=button_function2)
        button2.place(relx=0.5, rely=0.35, relwidth=.3, relheight=.2, anchor=tk.CENTER)

        # creates button number 3

        button3 = ctk.CTkButton(master=frame, text="placeholder", font=buttonfont, hover_color="green",
                                width=350, height=200, command=button_function3)
        button3.place(relx=0.5, rely=0.58, relwidth=.3, relheight=.2, anchor=tk.CENTER)

        # creates button number 4

        button4 = ctk.CTkButton(master=frame, text="Exit", font=buttonfont, hover_color="green",
                                width=350, height=200, command=exit_Button)
        button4.place(relx=0.50, rely=0.81, relwidth=.3, relheight=.2, anchor=tk.CENTER)


        frame.mainloop()

    def choiceGUI(self):
        #initializes variables needed for GUI display
        flashword, var1, var2, var3, var4, definition=self.variableinitialization()
        #creates frame for choice gui
        frame = ctk.CTkFrame(master=None, height=1000, width=1000)
        frame._state_before_windows_set_titlebar_color = 'zoomed'
        frame.pack(expand=1, fill="both")

        # creates font for flashcard
        flashfont = ctk.CTkFont(family="Times New Roman", size=75, weight="bold")
        # creates font for buttons
        buttonfont = ctk.CTkFont(family="Times New Roman", size=55, weight="bold")
        # creates back button font
        backbuttonfont = ctk.CTkFont(family="Times New Roman", size=25, weight="bold")

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
            frame.destroy()
            GUI.menuGUI(self)


        flashcard = ctk.CTkLabel(master=frame, text=flashword, text_color="black",
                                 font=flashfont, bg_color="white",
                                 width=800, height=500,
                                 fg_color="grey75", corner_radius=0,
                                 )
        flashcard.place(relx=0.5, rely=0.2, relwidth=.5, relheight=.3, anchor=tk.CENTER)

        # creates buttons for multiple choice selection

        button1 = ctk.CTkButton(master=frame, text=var1, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function1)
        button1.place(relx=0.25, rely=0.58, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates button number 2

        button2 = ctk.CTkButton(master=frame, text=var2, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function2)
        button2.place(relx=0.75, rely=0.58, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates button number 3

        button3 = ctk.CTkButton(master=frame, text=var3, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function3)
        button3.place(relx=0.25, rely=0.85, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates button number 4

        button4 = ctk.CTkButton(master=frame, text=var4, font=buttonfont, hover_color="green",
                                width=480, height=250, command=button_function4)
        button4.place(relx=0.75, rely=0.85, relwidth=.4, relheight=.25, anchor=tk.CENTER)

        # creates back button
        backbutton = ctk.CTkButton(master=frame, text="Back", font=backbuttonfont, hover_color="green",
                                   width=100, height=50, command=back_function)
        backbutton.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # prevents window from closing at the end of the code
        frame.mainloop()