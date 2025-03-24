import customtkinter
from customtkinter import *
import sys

user_color = sys.argv[2]
user_theme = sys.argv[3] 

#Making the text crisp
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

new_theme_mode = sys.argv[4]
if user_theme != new_theme_mode:
    user_theme = new_theme_mode

def change_appearance_mode_event(self, new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

w = customtkinter.CTk()
customtkinter.set_appearance_mode(user_theme)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(user_color)
w.geometry('450x600')
w.title('Study Buddy • Marks')
w.iconbitmap('icon.ico')
w.resizable(False,False)

l = customtkinter.CTkLabel(w, text='Name:')
l.pack(pady=1)
e = customtkinter.CTkEntry(w)
e.pack(pady=2)

l1 = customtkinter.CTkLabel(w, text='Subject 1:')
l1.pack(pady=1)
e1 = customtkinter.CTkEntry(w)
e1.pack(pady=2)

l2 = customtkinter.CTkLabel(w, text='Subject 2:')
l2.pack(pady=1)
e2 = customtkinter.CTkEntry(w)
e2.pack(pady=2)

l3 = customtkinter.CTkLabel(w, text='Subject 3:')
l3.pack(pady=1)
e3 = customtkinter.CTkEntry(w)
e3.pack(pady=2)

l4 = customtkinter.CTkLabel(w, text='Subject 4:')
l4.pack(pady=1)
e4 = customtkinter.CTkEntry(w)
e4.pack(pady=2)

l5 = customtkinter.CTkLabel(w, text='Subject 5:')
l5.pack(pady=1)
e5 = customtkinter.CTkEntry(w)
e5.pack(pady=2)

l0 = customtkinter.CTkLabel(w, text='Total marks')
l0.pack(pady=1)
e0 = customtkinter.CTkEntry(w)
e0.pack(pady=2)

def sub():
    l6.configure(text=e.get())
    l7.configure(text='Percentage: ' + f'{(int(str(e1.get()))+int(str(e2.get()))+int(str(e3.get()))+int(str(e4.get()))+int(str(e5.get())))/(int(str(e0.get())))*100}'+'%')

l6 = customtkinter.CTkLabel(w, text='')
l6.pack(pady=1)
l7 = customtkinter.CTkLabel(w, text='')
l7.pack(pady=1)

btn = customtkinter.CTkButton(w, text='Submit', command=sub)
btn.pack(pady=1)

appearance_mode_label = customtkinter.CTkLabel(w, text="Appearance Mode:", anchor="w")
appearance_mode_label.pack(pady=1)
appearance_mode_optionemenu = customtkinter.CTkOptionMenu(w, values=["Light", "Dark", "System"],
                                                               command=lambda mode: change_appearance_mode_event(w, mode))
appearance_mode_optionemenu.pack(pady=1)

w.mainloop()