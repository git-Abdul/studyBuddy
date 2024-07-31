from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import customtkinter
import tkinter as tk
import sys
# Making the text crisp
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

user_color = sys.argv[2]
user_theme = sys.argv[3] 
new_appearance_mode = sys.argv[4]
print(user_theme)
print(new_appearance_mode)

screen = customtkinter.CTk()
screen.title('Study Buddy • Calculator')
screen.geometry("400x500")  # Smaller window size
screen.iconbitmap('icon.ico')
screen.resizable(False, False)

if user_theme != new_appearance_mode:
    user_theme = new_appearance_mode

customtkinter.set_appearance_mode(user_theme)
customtkinter.set_default_color_theme(user_color)

def getAppearanceMode(new_appearance_mode: str):
    pass

def click(number):
    global operator
    operator += str(number)
    tex.set(operator)

def clear():
    global operator
    operator = ''
    tex.set(operator)

def equal(event=None):
    global operator
    result = eval(operator)
    operator = str(result)
    tex.set(result)

tex = StringVar()
operator = ''

style = ttk.Style()
style.configure("TButton", padding=(30, 15), font=('Arial', 20))  # Increase font size
style.configure("screen", background='#1c1c1c')

# Typer
entry1 = ctk.CTkEntry(screen, justify='right', textvariable=tex, width=400, font=('Arial', 60))  # Increase width and font size
entry1.grid(row=0, columnspan=4, padx=10, pady=10)
entry1.bind("<Return>", equal)

# Buttons
# Row 1
btn7 = ctk.CTkButton(screen, text='7', command=lambda: click(7), font=('Arial', 30))
btn7.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

btn8 = ctk.CTkButton(screen, text='8', command=lambda: click(8), font=('Arial', 30))
btn8.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

btn9 = ctk.CTkButton(screen, text='9', command=lambda: click(9), font=('Arial', 30))
btn9.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

btnadd = ctk.CTkButton(screen, text='+', command=lambda: click('+'), font=('Arial', 30))
btnadd.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

# Row 2
btn4 = ctk.CTkButton(screen, text='4', command=lambda: click(4), font=('Arial', 30))
btn4.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

btn5 = ctk.CTkButton(screen, text='5', command=lambda: click(5), font=('Arial', 30))
btn5.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

btn6 = ctk.CTkButton(screen, text='6', command=lambda: click(6), font=('Arial', 30))
btn6.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

btnsub = ctk.CTkButton(screen, text='-', command=lambda: click('-'), font=('Arial', 30))
btnsub.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

# Row 3
btn1 = ctk.CTkButton(screen, text='1', command=lambda: click(1), font=('Arial', 30))
btn1.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

btn2 = ctk.CTkButton(screen, text='2', command=lambda: click(2), font=('Arial', 30))
btn2.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

btn3 = ctk.CTkButton(screen, text='3', command=lambda: click(3), font=('Arial', 30))
btn3.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

btnmulti = ctk.CTkButton(screen, text='*', command=lambda: click('*'), font=('Arial', 30))
btnmulti.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

# Row 4
btn0 = ctk.CTkButton(screen, text='0', command=lambda: click(0), font=('Arial', 30))
btn0.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

btnclear = ctk.CTkButton(screen, text='C', command=clear, font=('Arial', 30))
btnclear.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

btnequal = ctk.CTkButton(screen, text='=', command=equal, font=('Arial', 30))
btnequal.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

btndiv = ctk.CTkButton(screen, text='/', command=lambda: click('/'), font=('Arial', 30))
btndiv.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

for i in range(5):
    screen.rowconfigure(i, weight=1)
for j in range(4):
    screen.columnconfigure(j, weight=1)

screen.mainloop()
