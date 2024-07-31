import customtkinter
import subprocess
import math
import os
import sys
from PIL import Image
import PIL.ImageOps
from win32mica import ApplyMica, MicaTheme, MicaStyle
import threading
from plyer import notification
from utils import logSignInSignOutTime, setUserColor, setUserTheme, reopen_window
import datetime
import sqlite3
import PIL.Image as Image

#Making the text crisp
from ctypes import windll, byref, c_int, sizeof
signed_in_user = sys.argv[1]
last_logout_time = sys.argv[2]
user_color = sys.argv[3]
user_theme = sys.argv[4]

print(signed_in_user, last_logout_time, user_color, user_theme)

global calculator
global planner
global notes
global charts
global marks
global timer
global browser
global bard
global stickynotes

def get_user_preferrences(uname):
    global calculator
    global planner
    global notes
    global charts
    global marks
    global timer
    global browser
    global bard
    global stickynotes
    # Connect to the SQLite database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Query data from the table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        user = row[1]
        if (user == uname):
            calculator = row[7]
            planner = row[8]
            notes = row[9]
            charts = row[10]
            marks = row[11]
            timer = row[12]
            browser = row[13]
            bard = row[14]
            stickynotes = row[15]
            print(calculator, planner, notes, charts, marks, timer, browser, bard, stickynotes)
            return True
        
    # Close the connection
    connection.close()

print(get_user_preferrences(signed_in_user))

#functions================================================================================================================================

def change_scaling_event(self, new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)
    
def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")
    
def Calc():
    subprocess.run(["python", "Calculator.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Calc():
    thread = threading.Thread(target=Calc)
    thread.start()

def Marks():
    subprocess.run(["python", "Marks.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Marks():
    thread = threading.Thread(target=Marks)
    thread.start()
    
def Chart():
    subprocess.run(["python", "Chart.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Chart():
    thread = threading.Thread(target=Chart)
    thread.start()

def Help():
    subprocess.run(['python', 'helpDesk.py', signed_in_user, user_color, user_theme, new_theme_mode])

def open_Help():
    thread = threading.Thread(target=Help)
    thread.start()
    
def Time():
    subprocess.run(['python', 'planner.py', signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Time():
    thread = threading.Thread(target=Time)
    thread.start()
    
def Timer():
    subprocess.run(['python', 'timer.py', signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Timer():
    thread = threading.Thread(target=Timer)
    thread.start()

def Notes():
    subprocess.run(["python", "notes.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Notes():
    thread = threading.Thread(target=Notes)
    thread.start()
    
def Web():
    subprocess.run(["python", "browser.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_web():
    thread = threading.Thread(target=Web)
    thread.start()
    
def Bard():
    subprocess.run(["python", "bard.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_bard():
    thread = threading.Thread(target=Bard)
    thread.start()
    
def Sticky():
    subprocess.run(["python", "stickyNotes.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Sticky():
    thread = threading.Thread(target=Sticky)
    thread.start()
    
def createNewTab():
    pass

#functions=====================================================================

customtkinter.set_appearance_mode(user_theme)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(user_color)

self = customtkinter.CTk()
global new_theme_mode 
new_theme_mode = user_theme

def change_appearance_mode_event(self, new_appearance_mode: str):
    global new_theme_mode 
    new_appearance_mode = new_appearance_mode.lower()
    new_theme_mode = new_appearance_mode
    customtkinter.set_appearance_mode(new_appearance_mode)
    setUserTheme(new_appearance_mode, signed_in_user)
    
def change_color_mode_event(new_color_mode: str):
    new_color_mode = new_color_mode.lower()
    setUserColor(new_color_mode, signed_in_user)
    reopen_window(self, signed_in_user, last_logout_time, new_color_mode, user_theme)

def callbackFunction(NewTheme):
    if NewTheme == MicaTheme.DARK:
        print("Theme has changed to dark!")
    else:
        print("Theme has changed to light!")
        
def open_home_window():
    global signed_in_user
    subprocess.run(["python", "signin.py"])
    self.withdraw()
         
def close_current_window(): 
    self.destroy()  
    open_home_window() 
        
def userLogout():
    logSignInSignOutTime(False, signed_in_user)
    self.after(1000, close_current_window)

#ApplyMica(HWND=parent_hwnd, Theme=mode, Style=style, OnThemeChange=callbackFunction)
self.title(f'Study Buddy - Hello {signed_in_user}')
self.iconbitmap('icon.ico')

Nunito = customtkinter.CTkFont(family="Nunito", size=24, weight="bold")

self.grid_columnconfigure(1, weight=1)
self.grid_columnconfigure((2,3), weight=0)
self.grid_rowconfigure((0, 1, 2, 4), weight=1)

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(35, 35))
self.bard = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bard.png")), size=(22,22))
self.web = customtkinter.CTkImage(Image.open(os.path.join(image_path, "webview.png")), size=(22,22))
self.notes = customtkinter.CTkImage(Image.open(os.path.join(image_path, "notes.png")), size=(22,22))
self.timer = customtkinter.CTkImage(Image.open(os.path.join(image_path, "timer.png")), size=(22,22))
self.planner = customtkinter.CTkImage(Image.open(os.path.join(image_path, "planner.png")), size=(22,22))
self.marks = customtkinter.CTkImage(Image.open(os.path.join(image_path, "marks.png")), size=(22,22))
self.plotter = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plotter.png")), size=(22,22))
self.calc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calc.png")), size=(22,22))
self.placeHolder = customtkinter.CTkImage(Image.open(os.path.join(image_path, "placeHolder.png")), size=(22,22))
self.logout = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logout.png")), size=(22,22))

self.plusIcon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plus.png")), size=(15,15))

self.btnCalc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calc.png")), size=(32,32))
self.btnPlanner = customtkinter.CTkImage(Image.open(os.path.join(image_path, "planner.png")), size=(32,32))
self.btnNotes = customtkinter.CTkImage(Image.open(os.path.join(image_path, "notes.png")), size=(32,32))
self.btnTimer = customtkinter.CTkImage(Image.open(os.path.join(image_path, "timer.png")), size=(32,32))
self.btnGraph = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plotter.png")), size=(32,32))
self.btnMarks = customtkinter.CTkImage(Image.open(os.path.join(image_path, "marks.png")), size=(32,32))
self.btnBard = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bard.png")), size=(32,32))
self.btnWeb = customtkinter.CTkImage(Image.open(os.path.join(image_path, "webview.png")), size=(32,32))
self.btnSticky = customtkinter.CTkImage(Image.open(os.path.join(image_path, "sticky.png")), size=(32,32))
    
def newTabWindow():
    root = customtkinter.CTk()
    root.attributes("-topmost", True)
    root.iconbitmap("icon.ico")
    root.title(" ")
    root.resizable(False, False)
    root.geometry('550x62')
    
    center_window(root)
    
    hwnd = root.winfo_id().__int__()

    Font = customtkinter.CTkFont(
        size=20,
        family="Nunito",
    )
    
    if(user_color == "blue"):
        color = "#3b8ed0"
    elif(user_color == "dark-blue"):
        color = "#3a7ebf"
    else:
        color = "#2cc985"

    entry = customtkinter.CTkEntry(
        root, 
        width=550, 
        height=60, 
        font=Font,
        placeholder_text="  Launch an applet...",
        border_color=color
    )
    entry.grid(row=1)
    
    btnFont = customtkinter.CTkFont(family="Inter", size=15)
    
    bbox1 = customtkinter.CTkButton(root, command=open_Calc, corner_radius=5, text="Calculator", compound="left", height=30, font=btnFont)
    #bbox1.grid(pady=20, row=2, column=0, columnspan=1, sticky="sw", padx=8, ipady=10)
    
    Label = customtkinter.CTkLabel(
        root,
        text="Calculator",
        compound="left",
        width=534, 
        height=60,
        font=Font,
    )
    # Label.grid(row=2)
    
    def send(event=None):
        applet_name = entry.get().lower()
        if applet_name == "calculator":
            open_Calc()
            root.destroy()
        elif applet_name in ["graph", "plotter"]:
            open_Chart()
            root.destroy()
        elif applet_name in ["marks", "marks calculator"]:
            open_Marks()
            root.destroy()
        elif applet_name == "planner":
            open_Time()
            root.destroy()
        elif applet_name == "timer":
            open_Timer()
            root.destroy()
        elif applet_name == "notes":
            open_Notes()
            root.destroy()
        elif applet_name == "bard":
            open_bard()
            root.destroy()
        elif applet_name in ["sticky notes", "sticky"]:
            open_Sticky()
            root.destroy()
        elif applet_name in ["webview", "web"]:
            open_web()
            root.destroy()
        else:
            notification.notify(
                title="Invalid applet name",
                message="Use the help desk to know more about the applet names.",
                timeout=10,
                app_icon='icon.ico',
            )
    
    def destroy(event=None):
        root.destroy()
    
    root.bind("<FocusOut>", destroy)
    entry.bind("<Return>", send)
    root.bind("<Escape>", destroy)
    
    root.mainloop()

self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=10, height=700)
self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
self.sidebar_frame.grid_rowconfigure(6, weight=1)

self.bbox1 = customtkinter.CTkButton(self.sidebar_frame, command=open_Calc, corner_radius=5, image=self.btnCalc, text="", compound="left", width=45, height=45)
self.bbox1.grid(pady=20, row=0, column=0, columnspan=1, sticky="sw", padx=8)

self.bbox2 = customtkinter.CTkButton(self.sidebar_frame, anchor="center", command=open_Time, corner_radius=5, image=self.btnPlanner, text="", compound="left", width=45, height=45)
self.bbox2.grid(pady=20, row=0, padx=1)

self.bbox3 = customtkinter.CTkButton(self.sidebar_frame, command=open_Notes, corner_radius=5, image=self.btnNotes, text="", compound="left", width=45, height=45)
self.bbox3.grid(pady=20, row=0, sticky="e", padx=10)

self.bbox4 = customtkinter.CTkButton(self.sidebar_frame, command=open_Chart, corner_radius=5, image=self.btnGraph, text="", compound="left", width=45, height=45)
self.bbox4.grid(row=1, column=0, columnspan=1, sticky="sw", padx=8)
self.bbox5 = customtkinter.CTkButton(self.sidebar_frame, anchor="center", command=open_Marks, corner_radius=5, image=self.btnMarks, text="", compound="left", width=45, height=45)
self.bbox5.grid(row=1, padx=1)
self.bbox6 = customtkinter.CTkButton(self.sidebar_frame, command=open_Timer, corner_radius=5, image=self.btnTimer, text="", compound="left", width=45, height=45)
self.bbox6.grid(row=1, sticky="e", padx=10)

self.bbox7 = customtkinter.CTkButton(self.sidebar_frame, command=open_web, corner_radius=5, image=self.btnWeb, text="", compound="left", width=45, height=45)
self.bbox7.grid(pady=20, row=2, column=0, columnspan=1, sticky="sw", padx=8)
self.bbox8 = customtkinter.CTkButton(self.sidebar_frame, anchor="center", command=open_bard, corner_radius=5, image=self.btnBard, text="", compound="left", width=45, height=45)
self.bbox8.grid(pady=20, row=2, padx=1)

self.bbox9 = customtkinter.CTkButton(self.sidebar_frame, command=open_Sticky, corner_radius=5, image=self.btnSticky, text="", compound="left", width=45, height=45)
self.bbox9.grid(pady=20, row=2, sticky="e", padx=10)

if calculator == 0:
    self.bbox1.configure(state="disabled", fg_color="#747474")
if planner == 0:
    self.bbox2.configure(state="disabled", fg_color="#747474")
if notes == 0:
    self.bbox3.configure(state="disabled", fg_color="#747474")
if charts == 0:
    self.bbox4.configure(state="disabled", fg_color="#747474")
if marks == 0:
    self.bbox5.configure(state="disabled", fg_color="#747474")
if timer == 0:
    self.bbox6.configure(state="disabled", fg_color="#747474")
if browser == 0:
    self.bbox7.configure(state="disabled", fg_color="#747474")
if bard == 0:
    self.bbox8.configure(state="disabled", fg_color="#747474")
if stickynotes == 0:
    self.bbox9.configure(state="disabled", fg_color="#747474")

self.newTab = customtkinter.CTkButton(self.sidebar_frame, corner_radius=5, text=" New tab", image=self.plusIcon, compound="left", command=newTabWindow, font=customtkinter.CTkFont(family="Inter", size=16))
self.newTab.grid(row=5, column=0, pady=30, ipady=10, ipadx=15)

# Set uniform padding between buttons
self.sidebar_frame.grid_rowconfigure((10, 6), weight=0)
self.sidebar_frame.grid_rowconfigure(10, weight=1)

self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:")
self.appearance_mode_label.grid(row=10, column=0, padx=20, pady=(210, 0))

self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                            command=lambda mode: change_appearance_mode_event(self, mode))
self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))

self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Blue", "Dark-Blue", "Green"],
                                                            command=lambda mode: change_color_mode_event(mode))
self.appearance_mode_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 10))

self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=lambda mode: change_scaling_event(self, mode))
self.scaling_optionemenu.grid(row=13, column=0, padx=20, pady=(10, 10))

self.btnLogout = customtkinter.CTkButton(self.sidebar_frame, text="Logout", image=self.logout, compound='left', fg_color="#cf352e", hover_color="#B02B25", command=userLogout)
self.btnLogout.grid(row=14, column=0, padx=20, pady=(10, 20))

# create main entry and button
self.entry = customtkinter.CTkEntry(self, placeholder_text='Facing any issues? Open the help desk for more information about the application!')
self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

self.main_button_1 = customtkinter.CTkButton(master=self,text='Open Help desk', command=open_Help)
self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

self.body = customtkinter.CTkFrame(self, width=500, height=600)  # Increase the height to make the textbox bigger
self.body.grid(row=0, column=1,columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
self.body.grid_rowconfigure(0, weight=1)  # Allow the textbox to expand vertically
self.body.grid_columnconfigure(0, weight=1)

if(user_color == "blue"):
    color = "#3b8ed0"
elif(user_color == "dark-blue"):
    color = "#3a7ebf"
else:
    color = "#2cc985"

self.label_frame = customtkinter.CTkFrame(self.body, fg_color=color)
self.label_frame.pack(fill="x", pady=10, padx=20)

self.helloText = customtkinter.CTkLabel(self.label_frame, text=f"Signed in as: {signed_in_user}", font=customtkinter.CTkFont(family="Nunito", size=17), text_color="white")
self.helloText.grid(row=0, column=0, columnspan=2, pady=10, padx=(10, 60))

if last_logout_time == "":
    lblText = "N/A"
else:
    lblText = last_logout_time

self.timeText = customtkinter.CTkLabel(self.label_frame, text=f"Last logged in: {lblText}", font=customtkinter.CTkFont(family="Nunito", size=17), text_color="white")
self.timeText.grid(row=0, column=5, columnspan=1, pady=10, padx=(460, 10))

if(user_color == 'green'):
    img_name = 'logoGreen.png'
elif(user_color == 'blue'):
    img_name = 'logoBlue.png'
else:
    img_name = 'logoDBlue.png'

self.home_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, img_name)), 
                                         size=(320, 320))
self.home_text = customtkinter.CTkLabel(self.body, text="", image=self.home_image, compound="center", font=Nunito) 
self.home_text.pack(pady=80)
#default values: 
self.entry.configure(state='disabled')

self.mainloop()