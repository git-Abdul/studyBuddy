import sqlite3
import customtkinter
import subprocess
import os
from PIL import Image
from plyer import notification
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
            
    def CreateUser(uname, pwd):
        # Connect to the SQLite database
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        #cursor.execute("DROP TABLE users")

        # Insert data into the table
        cursor.execute("INSERT INTO users (username, password, signInTime, signOutTime, usercolor, usertheme, calculator, planner, notes, chart, marks, timer, browser, bard, sticky) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f'{uname}', f'{pwd}', '', '', 'blue', 'light', calculator_var.get(), planner_var.get(), notes_var.get(), chart_var.get(), marks_var.get(), timer_var.get(), browser_var.get(), bard_var.get(), snotes_var.get()))
        
        # Commit the changes
        connection.commit()
            
        # Close the connection
        connection.close()
        
    w = customtkinter.CTk()
    w.geometry("385x500")
    w.title("Study Buddy - SignUp")
    w.iconbitmap('icon.ico')
    w.resizable(False, False)

    def open_home_window():
        global signed_in_user
        subprocess.run(["python", "home.py", signed_in_user, "", "blue", "light"])
        w.withdraw()
            
    def close_current_window():  # Cancel the scheduled closing
        w.destroy()  # Close the current window
        open_home_window()  # Open a new window
        
    def is_alphanumeric(text):
        return text.isalnum()

    def cmdSignUpClick():
        global signed_in_user
        print(userName.get(), passwordEntry.get())   
        uname = userName.get().lower()
        pwd = passwordEntry.get()
        if(is_alphanumeric(uname) == True):
            CreateUser(uname, pwd)
            signed_in_user = uname
            w.after(1000, close_current_window)
        else:
            notification.notify(
                app_icon = "icon.ico",
                title="Invalid Username.",
                message="Please enter a valid username.",
                timeout=5
            )
        print(planner_var.get())

    def toggle_password_visibility():
        global password_visible
        password_visible = not password_visible
        if password_visible:
            passwordEntry.configure(show="")
        else:
            passwordEntry.configure(show="•")
            
    def clearEntry():
        passwordEntry.delete(0, 'end')
        userName.delete(0, 'end')

    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
    w.show_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "show.png")), size=(15, 15))

    userNameLabel = customtkinter.CTkLabel(w, text="Enter Username:")
    userNameLabel.grid(row=0, column=0, pady=(30, 0))

    userName=customtkinter.CTkEntry(w, placeholder_text="Enter Username")
    userName.grid(row=0, column=1, pady=(30, 0))

    password_visible = False

    passwordLabel = customtkinter.CTkLabel(w, text="Enter Password:")
    passwordLabel.grid(row=1, column=0, pady=10)

    passwordEntry = customtkinter.CTkEntry(w, placeholder_text="Enter Password", show="•")
    passwordEntry.grid(row=1, column=1, padx=(5, 5))

    show_hide_button = customtkinter.CTkButton(w, command=toggle_password_visibility, image=w.show_image, text=None, width=15, height=27, fg_color="#444444", hover_color="#212121")
    show_hide_button.grid(row=1, column=2)

    boxFrame = customtkinter.CTkFrame(w)
    boxFrame.grid(sticky="nsew", columnspan=3, padx=(25, 20), pady=(20, 15), row=2)

    lblPreferences = customtkinter.CTkLabel(boxFrame, text="Module Preferences", font=customtkinter.CTkFont(family="Inter", size=17))
    lblPreferences.pack(pady=(3, 0), padx=10)

    innerFrame = customtkinter.CTkFrame(boxFrame)
    innerFrame.pack(padx=(25, 20), pady=(20, 20))

    def calculator_event():
        print("checkbox toggled, current value:", calculator_var.get())
    calculator_var = customtkinter.StringVar(value=0)

    calculator = customtkinter.CTkCheckBox(innerFrame, text="Calculator", onvalue=1, offvalue=0, variable=calculator_var, command=calculator_event)
    calculator.grid(pady=10, padx=10, row=0, column=0)

    pl = customtkinter.CTkLabel(innerFrame, text=" ")
    pl.grid(pady=10, padx=10, row=0, column=1)

    def planner_event():
        print("checkbox toggled, current value:", planner_var.get())
    planner_var = customtkinter.StringVar(value=0)

    planner = customtkinter.CTkCheckBox(innerFrame, text="Planner", onvalue=1, offvalue=0, variable=planner_var, command=planner_event)
    planner.grid(pady=10, padx=10, row=0, column=2)

    def notes_event():
        print("checkbox toggled, current value:", notes_var.get())
    notes_var = customtkinter.StringVar(value=0)

    notes = customtkinter.CTkCheckBox(innerFrame, text="Notes", onvalue=1, offvalue=0, variable=notes_var, command=notes_event)
    notes.grid(pady=10, padx=10, row=1, column=0)

    pl = customtkinter.CTkLabel(innerFrame, text=" ")
    pl.grid(pady=10, padx=10, row=1, column=1)

    def chart_event():
        print("checkbox toggled, current value:", chart_var.get())
    chart_var = customtkinter.StringVar(value=0)

    chart = customtkinter.CTkCheckBox(innerFrame, text="Chart", onvalue=1, offvalue=0, variable=chart_var, command=chart_event)
    chart.grid(pady=10, padx=10, row=1, column=2)

    def marks_event():
        print("checkbox toggled, current value:", marks_var.get())
    marks_var = customtkinter.StringVar(value=0)

    marks = customtkinter.CTkCheckBox(innerFrame, text="Marks", onvalue=1, offvalue=0, variable=marks_var, command=marks_event)
    marks.grid(pady=10, padx=10, row=2, column=0)

    pl = customtkinter.CTkLabel(innerFrame, text=" ")
    pl.grid(pady=10, padx=10, row=2, column=1)

    def timer_event():
        print("checkbox toggled, current value:", timer_var.get())
    timer_var = customtkinter.StringVar(value=0)

    timer = customtkinter.CTkCheckBox(innerFrame, text="Timer", onvalue=1, offvalue=0, variable=timer_var, command=timer_event)
    timer.grid(pady=10, padx=10, row=2, column=2)

    def browser_event():
        print("checkbox toggled, current value:", browser_var.get())
    browser_var = customtkinter.StringVar(value=0)

    browser = customtkinter.CTkCheckBox(innerFrame, text="Browser", onvalue=1, offvalue=0, variable=browser_var, command=browser_event)
    browser.grid(pady=10, padx=10, row=3, column=0)

    pl = customtkinter.CTkLabel(innerFrame, text=" ")
    pl.grid(pady=10, padx=10, row=3, column=1)

    def snotes_event():
        print("checkbox toggled, current value:", snotes_var.get())
    snotes_var = customtkinter.StringVar(value=0)

    stickynotes = customtkinter.CTkCheckBox(innerFrame, text="StickyNotes", onvalue=1, offvalue=0, variable=snotes_var, command=snotes_event)
    stickynotes.grid(pady=10, padx=10, row=3, column=2)

    def bard_event():
        print("checkbox toggled, current value:", bard_var.get())
    bard_var = customtkinter.StringVar(value=0)

    bard = customtkinter.CTkCheckBox(innerFrame, text="Bard", onvalue=1, offvalue=0, variable=bard_var, command=bard_event)
    bard.grid(pady=10, padx=10, row=4, column=0)

    pl = customtkinter.CTkLabel(innerFrame, text=" ")
    pl.grid(pady=10, padx=10, row=3, column=1)

    def selectAll_event():
        print("checkbox toggled, current value:", selectAll_var.get())
        toggle_All()
    selectAll_var = customtkinter.StringVar(value=0)

    selectAll = customtkinter.CTkCheckBox(innerFrame, text="Select All", onvalue=1, offvalue=0, variable=selectAll_var, command=selectAll_event)
    selectAll.grid(pady=10, padx=10, row=4, column=2)

    def toggle_All():
        state = selectAll_var.get()
        if(state == "1"):
            calculator.select()
            planner.select()
            notes.select()
            marks.select()
            chart.select()
            browser.select()
            timer.select()
            bard.select()
            stickynotes.select()
        else:
            calculator.deselect()
            planner.deselect()
            notes.deselect()
            chart.deselect()
            marks.deselect()
            timer.deselect()
            browser.deselect()
            stickynotes.deselect()
            bard.deselect()

    signUp = customtkinter.CTkButton(w, text="Sign Up", width=100, command=cmdSignUpClick, fg_color="#444444", hover_color="#212121")
    signUp.grid(row=3, column=0, pady=10, padx=(60, 20))
    clear = customtkinter.CTkButton(w, text="Clear", width=100, command=clearEntry, fg_color="#444444", hover_color="#212121")
    clear.grid(row=3, column=1, pady=10, padx=30)
    
    w.mainloop()
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
