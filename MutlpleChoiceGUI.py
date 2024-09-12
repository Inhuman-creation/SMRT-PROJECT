import customtkinter as ctk
import tkinter as tk
from InitializationFunctions import variableinitialization


#NEED TO CREATE A FUNCTION WHICH CALLS MAIN AND INITIALIZES VARIABLES
flashword,var1,var2,var3,var4=variableinitialization()

#creates function for button to work
def button_function1():
    print(var1)

def button_function2():
    print(var2)

def button_function3():
    print(var3)

def button_function4():
    var4="it works"
    button4.configure(text=var4)
    print(var4)


#creates main window
app=ctk.CTk()
app.geometry('1000x1000')
app.title("SMRT")

#creates font for flashcard
flashfont=ctk.CTkFont(family="Times New Roman", size=65, weight="bold")
#creates font for buttons
buttonfont=ctk.CTkFont(family="Times New Roman", size=55, weight="bold")
#creates frame for flash card
frame=ctk.CTkFrame(master=app,width=800,height=400,
                    corner_radius=0,bg_color="transparent")

frame.pack(padx=20,pady=20)

#flashcard framework
flashcard=ctk.CTkLabel(master=frame,text=flashword,text_color="black",
                       font=flashfont,bg_color="white",
                       width=600,height=300,
                       fg_color="grey75",corner_radius=0,
                       )
flashcard.grid(padx=20,pady=10)
#sets appearance mode dark
ctk.set_appearance_mode("Dark")

#sets default color theme
ctk.set_default_color_theme("blue")

#creates a button for multiple choice selection

button1=ctk.CTkButton(master=app,text=var1,font=buttonfont, hover_color="green",
                      width=480,height=250, command=button_function1)
button1.place(relx=0.25,rely=0.58,anchor=tk.CENTER)

#creates button number 2

button2=ctk.CTkButton(master=app,text=var2,font=buttonfont, hover_color="green",
                      width=480,height=250, command=button_function2)
button2.place(relx=0.75,rely=0.58,anchor=tk.CENTER)

#creates button number 3

button3=ctk.CTkButton(master=app,text=var3,font=buttonfont, hover_color="green",
                      width=480,height=250, command=button_function3)
button3.place(relx=0.25,rely=0.85,anchor=tk.CENTER)


#creates button number 4

button4=ctk.CTkButton(master=app,text=var4,font=buttonfont, hover_color="green",
                      width=480,height=250, command=button_function4)
button4.place(relx=0.75,rely=0.85,anchor=tk.CENTER)


#this command is so the window does not close once running through intial code
app.mainloop()


