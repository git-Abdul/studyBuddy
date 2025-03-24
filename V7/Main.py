import sqlite3
import customtkinter
import subprocess
import os
from PIL import Image
from win32mica import ApplyMica, MicaTheme, MicaStyle

# Define the logSignInSignOutTime function
def logSignInSignOutTime(signIn, user):
    # Implement the logging functionality here
    if signIn:
        print(f"User {user} signed in.")
    else:
        print(f"User {user} signed out.")

global password_visible
global signed_in_user
global userColor
global lastLogOutTime
global userTheme
global dropdown_visible
signed_in_user = None
userTheme = 'Light'
userColor = 'blue'
lastLogOutTime = None
dropdown_visible = False

def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")

def close_current_window():
    w.destroy()
    open_home_window()

def isValidSignIn(uname, pwd):
    global lastLogOutTime, userColor, userTheme
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        user = row[1]
        pword = row[2]
        lastLogOutTime = row[4]
        userColor = row[5]
        userTheme = row[6]
        if (user == uname and pword == pwd):
            return True
    connection.close()
    return False

w = customtkinter.CTk()
w.title("Study Buddy • SignIn")
w.iconbitmap('icon.ico')

# Set window to full screen (we’re going all out)
w.attributes("-fullscreen", True)
customtkinter.set_appearance_mode("System")

# --- Top Bar Setup (Arc Browser Style) ---
top_bar = customtkinter.CTkFrame(w, height=60, fg_color="transparent", corner_radius=0)
top_bar.pack(side="top", fill="x")

# Function to toggle the dropdown menu
def toggle_dropdown():
    global dropdown_visible
    if dropdown_visible:
        dropdown_menu.place_forget()
        dropdown_visible = False
    else:
        # Place dropdown menu just below the avatar button
        x = avatar_button.winfo_x()
        y = avatar_button.winfo_y() + avatar_button.winfo_height()
        dropdown_menu.place(x=x, y=y)
        dropdown_visible = True

# Sample callback when a dropdown option is selected
def on_task_selected(choice):
    print(f"Selected task: {choice}")
    # Hide dropdown after selection
    toggle_dropdown()

# Create a circular avatar button with the user's initial (defaulting to "A")
# (Using corner_radius equal to half the width for a circular effect)
avatar_button = customtkinter.CTkButton(top_bar,
                                        text="A",  # default initial; update this after sign-in if needed
                                        width=40, height=40,
                                        corner_radius=20,
                                        fg_color="#4a90e2",
                                        text_color="white",
                                        font=customtkinter.CTkFont(size=16, weight="bold"),
                                        command=toggle_dropdown)
avatar_button.place(x=20, y=10)

# Create a dropdown menu using CTkOptionMenu; initially hidden
dropdown_menu = customtkinter.CTkOptionMenu(top_bar,
                                            values=["Task 1", "Task 2", "Task 3"],
                                            command=on_task_selected,
                                            width=120)
# Do not place it yet; it'll be toggled via the avatar button

# --- Main Content (Sign In Frame) ---
# For balance, we center the sign-in frame on the remaining part of the screen.
login_frame = customtkinter.CTkFrame(w, corner_radius=10)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Logo image and sign-in label
current_path = os.path.dirname(os.path.realpath(__file__))
logo_image = customtkinter.CTkImage(Image.open(os.path.join(current_path, "_images/logo.png")), size=(80, 80))
login_label = customtkinter.CTkLabel(login_frame, text="", image=logo_image, font=customtkinter.CTkFont(weight="bold", size=10, family="Inter"), compound="top")
login_label.grid(row=0, column=0, padx=30, pady=(150, 15))

username_entry = customtkinter.CTkEntry(login_frame, width=200, placeholder_text="Username")
username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
password_entry = customtkinter.CTkEntry(login_frame, width=200, show="•", placeholder_text="Password")
password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))

def open_signUp_window():
    subprocess.run(["python", "signup.py"])
    w.withdraw()

def close_current_window2():
    w.destroy()
    open_signUp_window()

def cmdSignUpClick():
    w.after(1000, close_current_window2)

def open_home_window():
    global signed_in_user, lastLogOutTime
    subprocess.run(["python", "home.py", signed_in_user, lastLogOutTime, userColor, userTheme])
    w.withdraw()

def cmdSignInClick():
    global signed_in_user
    uname = username_entry.get()
    pwd = password_entry.get()
    validUser = isValidSignIn(uname, pwd)
    if not validUser:
        username_entry.configure(border_color="red")
        password_entry.configure(border_color="red")
    else:
        signed_in_user = uname
        # Update avatar with the first letter of the signed in user
        avatar_button.configure(text=uname[0].upper())
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
    username_entry.configure(border_color="#979da2")
    password_entry.configure(border_color="#979da2")

def on_pwd_focus_in(event):
    password_entry.configure(border_color="#979da2")
    username_entry.configure(border_color="#979da2")

username_entry.bind("<FocusIn>", on_uname_focus_in)
username_entry.bind("<Escape>", clearEntry)
password_entry.bind("<FocusIn>", on_pwd_focus_in)
password_entry.bind("<Escape>", clearEntry)

username_entry.insert("end", "admin")
password_entry.insert("end", "admin")

login_button = customtkinter.CTkButton(login_frame, text="Login", width=200, command=cmdSignInClick)
login_button.grid(row=3, column=0, padx=30, pady=(15, 15))
signUp_button = customtkinter.CTkButton(login_frame, text="Sign Up", width=200, command=close_current_window2)
signUp_button.grid(row=4, column=0, padx=30, pady=(0, 15))

center_window(w)
w.mainloop()