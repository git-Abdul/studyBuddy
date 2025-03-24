import sqlite3
import customtkinter
import subprocess
import os
import hashlib, binascii
from win32mica import ApplyMica, MicaTheme, MicaStyle

def logSignInSignOutTime(signIn, user):
    if signIn:
        print(f"User {user} signed in.")
    else:
        print(f"User {user} signed out.")

# ---------------------------
# Password Encryption Helpers
# ---------------------------
def hash_password(password, salt=None):
    """Hash a password using PBKDF2 (SHA256) with a salt."""
    if not salt:
        salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Store as hex strings separated by $
    return binascii.hexlify(salt).decode('ascii') + "$" + binascii.hexlify(pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    try:
        salt_str, pwdhash_str = stored_password.split("$")
        salt = binascii.unhexlify(salt_str)
        pwdhash = binascii.unhexlify(pwdhash_str)
        new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return new_hash == pwdhash
    except Exception as e:
        print("Password verification error:", e)
        return False

# ---------------------------
# Database Functions
# ---------------------------
def init_db():
    """Create users table if it doesn't exist."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            dummy1 TEXT,
            lastLogOutTime TEXT,
            userColor TEXT,
            userTheme TEXT
        )
    ''')
    connection.commit()
    connection.close()

def add_user(username, password, userColor="blue", userTheme="Light"):
    """Add a new user with encrypted password to the database."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    enc_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, userColor, userTheme) VALUES (?, ?, ?, ?)",
                       (username, enc_password, userColor, userTheme))
        connection.commit()
        print(f"User {username} added successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    connection.close()

def isValidSignIn(uname, pwd):
    """Check if the provided username and password match the encrypted database entry."""
    global lastLogOutTime, userColor, userTheme
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (uname,))
    row = cursor.fetchone()
    if row is None:
        connection.close()
        return False
    stored_password = row[2]
    if verify_password(stored_password, pwd):
        lastLogOutTime = row[4]
        userColor = row[5]
        userTheme = row[6]
        connection.close()
        return True
    connection.close()
    return False

# Initialize database (creates table if needed)
init_db()
# Uncomment the following line to add a default user for testing:
# add_user("admin", "admin")

# ---------------------------
# Main Application UI
# ---------------------------
global password_visible
global signed_in_user
global lastLogOutTime
global userTheme
global userColor
global dropdown_visible
signed_in_user = None
userTheme = 'Light'
userColor = 'blue'
lastLogOutTime = None
dropdown_visible = False

# Track full screen toggle state
full_screen = True

def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")

def close_current_window():
    # Instead of destroying the main window, simply hide it
    w.withdraw()
    open_home_window()

# ---------------------------
# Signup Window (Toplevel)
# ---------------------------
def show_signup_window():
    # Create a new Toplevel window for signup without closing the main window
    signup_win = customtkinter.CTkToplevel(w)
    signup_win.title("Sign Up")
    signup_win.geometry("400x300")
    
    # Center the signup window
    screen_width = signup_win.winfo_screenwidth()
    screen_height = signup_win.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 300) // 2
    signup_win.geometry(f"400x300+{x}+{y}")
    
    # Create a signup frame inside the new window
    signup_frame = customtkinter.CTkFrame(signup_win)
    signup_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Header label
    header = customtkinter.CTkLabel(signup_frame, text="Create a New Account", font=customtkinter.CTkFont(size=20, weight="bold"))
    header.pack(pady=10)
    
    # Username entry
    username_label = customtkinter.CTkLabel(signup_frame, text="Username:")
    username_label.pack(pady=(10, 0))
    username_entry_signup = customtkinter.CTkEntry(signup_frame, placeholder_text="Enter username")
    username_entry_signup.pack(pady=5)
    
    # Password entry
    password_label = customtkinter.CTkLabel(signup_frame, text="Password:")
    password_label.pack(pady=(10, 0))
    password_entry_signup = customtkinter.CTkEntry(signup_frame, placeholder_text="Enter password", show="•")
    password_entry_signup.pack(pady=5)
    
    # Sign Up button callback
    def register():
        new_username = username_entry_signup.get().strip()
        new_password = password_entry_signup.get().strip()
        if new_username and new_password:
            add_user(new_username, new_password)
            print(f"User '{new_username}' registered successfully.")
            signup_win.destroy()  # Close the signup window after successful registration.
        else:
            print("Please fill in both username and password.")
    
    signup_btn = customtkinter.CTkButton(signup_frame, text="Sign Up", command=register)
    signup_btn.pack(pady=20)

# ---------------------------
# Home Window (Toplevel)
# ---------------------------
def open_home_window():
    # Create a new Toplevel window as the Home interface.
    home_win = customtkinter.CTkToplevel(w)
    home_win.title("Study Buddy • Home")
    home_win.geometry("800x600")
    home_label = customtkinter.CTkLabel(home_win, text=f"Welcome {signed_in_user}!", font=customtkinter.CTkFont(size=24, weight="bold"))
    home_label.pack(pady=20)

# ---------------------------
# UI: Create the main window
# ---------------------------
w = customtkinter.CTk()
w.title("Study Buddy • SignIn")
# Removed external icon dependency

# Set window to full screen
w.attributes("-fullscreen", True)
customtkinter.set_appearance_mode("System")

# --- Top Bar Setup (Arc Browser Style) ---
top_bar = customtkinter.CTkFrame(w, height=60, fg_color="transparent", corner_radius=0)
top_bar.pack(side="top", fill="x")

# --- Window Control Buttons ---
def minimize_window():
    w.iconify()

def maximize_window():
    if w.state() == "normal":
        w.state("zoomed")
    else:
        w.state("normal")

def toggle_fullscreen():
    global full_screen
    full_screen = not full_screen
    w.attributes("-fullscreen", full_screen)

window_control_frame = customtkinter.CTkFrame(top_bar, fg_color="transparent", corner_radius=0)
window_control_frame.pack(side="right", padx=10, pady=10)

minimize_btn = customtkinter.CTkButton(window_control_frame,
                                       text="–",
                                       width=30, height=30,
                                       corner_radius=5,
                                       command=minimize_window)
minimize_btn.pack(side="left", padx=2)

maximize_btn = customtkinter.CTkButton(window_control_frame,
                                       text="▢",
                                       width=30, height=30,
                                       corner_radius=5,
                                       command=maximize_window)
maximize_btn.pack(side="left", padx=2)

fullscreen_btn = customtkinter.CTkButton(window_control_frame,
                                         text="⛶",
                                         width=30, height=30,
                                         corner_radius=5,
                                         command=toggle_fullscreen)
fullscreen_btn.pack(side="left", padx=2)

# --- Dropdown Menu and Avatar ---
def toggle_dropdown():
    global dropdown_visible
    if dropdown_visible:
        dropdown_menu.place_forget()
        dropdown_visible = False
    else:
        x = avatar_button.winfo_x()
        y = avatar_button.winfo_y() + avatar_button.winfo_height()
        dropdown_menu.place(x=x, y=y)
        dropdown_visible = True

def on_task_selected(choice):
    print(f"Selected task: {choice}")
    toggle_dropdown()

avatar_button = customtkinter.CTkButton(top_bar,
                                        text="A",
                                        width=40, height=40,
                                        corner_radius=20,
                                        fg_color="#4a90e2",
                                        text_color="white",
                                        font=customtkinter.CTkFont(size=16, weight="bold"),
                                        command=toggle_dropdown)
avatar_button.place(x=20, y=10)

dropdown_menu = customtkinter.CTkOptionMenu(top_bar,
                                            values=["Task 1", "Task 2", "Task 3"],
                                            command=on_task_selected,
                                            width=120)

# --- Main Content (Sign In Frame) ---
login_frame = customtkinter.CTkFrame(w, corner_radius=10)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

login_label = customtkinter.CTkLabel(login_frame, text="Study Buddy", font=customtkinter.CTkFont(size=24, weight="bold"))
login_label.grid(row=0, column=0, padx=30, pady=(30, 15))

username_entry = customtkinter.CTkEntry(login_frame, width=200, placeholder_text="Username")
username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
password_entry = customtkinter.CTkEntry(login_frame, width=200, show="•", placeholder_text="Password")
password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))

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

# Pre-fill entries for quick access in this corporate demo
username_entry.insert("end", "admin")
password_entry.insert("end", "admin")

login_button = customtkinter.CTkButton(login_frame, text="Login", width=200, command=cmdSignInClick)
login_button.grid(row=3, column=0, padx=30, pady=(15, 15))
# Set the Sign Up button to open the signup window without closing the main window
signUp_button = customtkinter.CTkButton(login_frame, text="Sign Up", width=200, command=show_signup_window)
signUp_button.grid(row=4, column=0, padx=30, pady=(0, 15))

center_window(w)
w.mainloop()
