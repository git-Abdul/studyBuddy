import sqlite3
import customtkinter
import subprocess
import os
from PIL import Image
from win32mica import ApplyMica, MicaTheme, MicaStyle
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
w.title("Study Buddy • SignIn")
w.iconbitmap('icon.ico')
center_window(w)

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
    print(username_entry.get(), password_entry.get())   
    uname = username_entry.get()
    pwd = password_entry.get()
    validUser = isValidSignIn(uname, pwd)
    print(validUser)
    
    if validUser == False:
        username_entry.configure(border_color="red")
        password_entry.configure(border_color="red")
    else:
        signed_in_user = uname
        logSignInSignOutTime(True, signed_in_user)
        w.after(1000, close_current_window)

def toggle_password_visibility():
    global password_visible
    password_visible = not password_visible
    if password_visible:
        password_entry.configure(show="")
    else:
        password_entry.configure(show="•")
        
def clearEntry(event=None):
    customtkinter.set_default_color_theme("green")
    password_entry.delete(0, 'end')
    username_entry.delete(0, 'end')
    

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
w.show_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "show.png")), size=(15, 15))

def on_uname_focus_in(event):
    username_entry.configure(border_color = "#979da2")
    password_entry.configure(border_color = "#979da2")
    
def on_pwd_focus_in(event):
    password_entry.configure(border_color = "#979da2")
    username_entry.configure(border_color = "#979da2")

w.title("StudyBuddy - Sign In")
w.geometry(f"900x600")
w.resizable(False, False)
customtkinter.set_appearance_mode("System")

current_path = os.path.dirname(os.path.realpath(__file__))
bg_image = customtkinter.CTkImage(Image.open(current_path + "/_images/bg_gradient.jpg"), size=(900, 600))
bg_image_label = customtkinter.CTkLabel(w, image=bg_image)
bg_image_label.grid(row=0, column=0)

# create login frame
logo_image = customtkinter.CTkImage(Image.open(current_path + "/_images/logo.png"), size=(80, 80))
login_frame = customtkinter.CTkFrame(w, corner_radius=10)
login_frame.grid(row=0, column=0, sticky="ns")
login_label = customtkinter.CTkLabel(login_frame, text="", image=logo_image, font=customtkinter.CTkFont(weight="bold", size=10, family="Inter"), compound="top")
login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
username_entry = customtkinter.CTkEntry(
login_frame, width=200, placeholder_text="Username")
username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
password_entry = customtkinter.CTkEntry(
login_frame, width=200, show="•", placeholder_text="Password")
password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
login_button = customtkinter.CTkButton(
login_frame, text="Login", width=200, command=cmdSignInClick)
login_button.grid(row=3, column=0, padx=30, pady=(15, 15))
signUp_button = customtkinter.CTkButton(
login_frame, text="Sign Up", width=200, command=close_current_window2)
signUp_button.grid(row=4, column=0, padx=30, pady=(0, 15))

username_entry.bind("<FocusIn>", on_uname_focus_in)
username_entry.bind("<Escape>", clearEntry)

password_entry.bind("<FocusIn>", on_pwd_focus_in)
password_entry.bind("<Escape>", clearEntry)

username_entry.insert("end", "admin")
password_entry.insert("end", "admin")

# create main frame

# boxFrame = customtkinter.CTkFrame(w, width=200, height=20)
# boxFrame.grid(row=4, columnspan=3)
# boxFrame.grid_forget()

# lblSignInFailed = customtkinter.CTkLabel(boxFrame, text="    Sign In Failed.", text_color="red")
# lblSignInFailed.grid(row=4,columnspan=3, padx=(300, 0))
# lblSignInFailed.grid_forget()

center_window(w)
w.mainloop()
