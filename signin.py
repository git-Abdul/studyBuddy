import sqlite3
import customtkinter
import subprocess
import math
import os
from PIL import Image
import PIL.ImageOps
from win32mica import ApplyMica, MicaTheme, MicaStyle
import sys
import threading
from plyer import notification
import datetime
from utils import logSignInSignOutTime

global password_visible
global signed_in_user
global userColor
global lastLogOutTime
global userTheme
userTheme = 'Light'
userColor = 'blue'
lastLogOutTime = None
signed_in_user = None

def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")
    
    
def close_current_window():
    cancel_id = w.after(1000, close_current_window)
    w.after_cancel(cancel_id)  # Cancel the scheduled closing
    w.destroy()  # Close the current window   
        
def isValidSignIn(uname, pwd):
    global lastLogOutTime
    global userColor
    global userTheme
    # Connect to the SQLite database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Query data from the table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        user = row[1]
        pword = row[2]
        lastLogOutTime = row[4]
        userColor = row[5]
        userTheme = row[6]
        #print(user, pword)
        if (user == uname and pword == pwd):
            return True
        
    # Close the connection
    connection.close()

    return False
    
w = customtkinter.CTk()
w.geometry("390x200")
w.title("Study Buddy - SignIn")
w.iconbitmap('icon.ico')
w.resizable(False, False)

def open_signUp_window():
    global signed_in_user
    subprocess.run(["python", "signup.py"])
    w.withdraw()
    
def close_current_window2():  # Cancel the scheduled closing
    w.destroy()  # Close the current window
    open_signUp_window() 
    
def cmdSignUpClick():
    w.after(1000, close_current_window2)

def open_home_window():
    global signed_in_user
    global lastLogOutTime
    subprocess.run(["python", "home.py", signed_in_user, lastLogOutTime, userColor, userTheme])
    w.withdraw()
        
def close_current_window():  # Cancel the scheduled closing
    w.destroy()  # Close the current window
    open_home_window()  # Open a new window


def cmdSignInClick():
    global signed_in_user
    print(userName.get(), passwordEntry.get())   
    uname = userName.get()
    pwd = passwordEntry.get()
    validUser = isValidSignIn(uname, pwd)
    print(validUser)
    
    if validUser == False:
        userName.configure(border_color="red")
        passwordEntry.configure(border_color="red")
    else:
        signed_in_user = uname
        logSignInSignOutTime(True, signed_in_user)
        w.after(1000, close_current_window)

def toggle_password_visibility():
    global password_visible
    password_visible = not password_visible
    if password_visible:
        passwordEntry.configure(show="")
    else:
        passwordEntry.configure(show="•")
        
def clearEntry():
    customtkinter.set_default_color_theme("green")
    passwordEntry.delete(0, 'end')
    userName.delete(0, 'end')
    

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
w.show_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "show.png")), size=(15, 15))

userNameLabel = customtkinter.CTkLabel(w, text="Username:")
userNameLabel.grid(row=0, column=0, pady=(30, 0))

def on_uname_focus_in(event):
    userName.configure(border_color = "#979da2")
    passwordEntry.configure(border_color = "#979da2")
    
def on_pwd_focus_in(event):
    passwordEntry.configure(border_color = "#979da2")
    userName.configure(border_color = "#979da2")

userName=customtkinter.CTkEntry(w, placeholder_text="Enter Username")
userName.grid(row=0, column=1, pady=(30, 0))

password_visible = False

passwordLabel = customtkinter.CTkLabel(w, text="Password:")
passwordLabel.grid(row=1, column=0, pady=10)

passwordEntry = customtkinter.CTkEntry(w, placeholder_text="Enter Password", show="•")
passwordEntry.grid(row=1, column=1, padx=(5, 5))

userName.insert("end", "admin")
passwordEntry.insert("end", "admin")

userName.bind("<FocusIn>", on_uname_focus_in)
passwordEntry.bind("<FocusIn>", on_pwd_focus_in)

show_hide_button = customtkinter.CTkButton(w, command=toggle_password_visibility, image=w.show_image, text=None, width=15, height=27, fg_color="#444444", hover_color="#212121")
show_hide_button.grid(row=1, column=2)

signIn = customtkinter.CTkButton(w, text="Sign In", width=100, command=cmdSignInClick, fg_color="#444444", hover_color="#212121")
signIn.grid(row=2, column=0, pady=10, padx=(60, 20))

clear = customtkinter.CTkButton(w, text="Clear", width=100, command=clearEntry, fg_color="#444444", hover_color="#212121")
clear.grid(row=2, column=1, pady=10, padx=30)

btnSignUp = customtkinter.CTkButton(w, text="Sign Up", width=200, height=25, command=cmdSignUpClick, fg_color="#444444", hover_color="#212121")
btnSignUp.grid(row=3, column=0, columnspan=3, pady=10, padx=40, sticky="nsew")

# boxFrame = customtkinter.CTkFrame(w, width=200, height=20)
# boxFrame.grid(row=4, columnspan=3)
# boxFrame.grid_forget()

# lblSignInFailed = customtkinter.CTkLabel(boxFrame, text="    Sign In Failed.", text_color="red")
# lblSignInFailed.grid(row=4,columnspan=3, padx=(300, 0))
# lblSignInFailed.grid_forget()

center_window(w)
w.mainloop()
