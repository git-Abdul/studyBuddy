import customtkinter
import math
import subprocess
from tkinterweb import HtmlFrame
import webview
from tkinter import messagebox
import matplotlib.pyplot as plt
from google import genai
import sv_ttk
import tkinter as tk
from tkinter import ttk
from tkinter import *
import json
import os
import sys
import time
from PIL import Image, ImageTk
from win32mica import MicaTheme
import threading
from plyer import notification
from utils import logSignInSignOutTime, setUserColor, setUserTheme, reopen_window, reopen_signInPage
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
    
def raise_above_all(window):
    window.attributes('-topmost', True)
    window.attributes('-topmost', False)
    
def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")
    
def open_Calc():
    screen = customtkinter.CTk()
    screen.title('Study Buddy • Calculator')
    screen.geometry("400x500")  # Smaller window size
    screen.iconbitmap('icon.ico')
    screen.resizable(False, False)
    
    userTheme = user_theme
    new_appearance_mode = new_theme_mode

    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    customtkinter.set_appearance_mode(userTheme)
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
    entry1 = customtkinter.CTkEntry(screen, justify='right', textvariable=tex, width=400, font=('Arial', 60))  # Increase width and font size
    entry1.grid(row=0, columnspan=4, padx=10, pady=10)
    entry1.bind("<Return>", equal)

    # Buttons
    # Row 1
    btn7 = customtkinter.CTkButton(screen, text='7', command=lambda: click(7), font=('Arial', 30))
    btn7.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    btn8 = customtkinter.CTkButton(screen, text='8', command=lambda: click(8), font=('Arial', 30))
    btn8.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    btn9 = customtkinter.CTkButton(screen, text='9', command=lambda: click(9), font=('Arial', 30))
    btn9.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

    btnadd = customtkinter.CTkButton(screen, text='+', command=lambda: click('+'), font=('Arial', 30))
    btnadd.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

    # Row 2
    btn4 = customtkinter.CTkButton(screen, text='4', command=lambda: click(4), font=('Arial', 30))
    btn4.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    btn5 = customtkinter.CTkButton(screen, text='5', command=lambda: click(5), font=('Arial', 30))
    btn5.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    btn6 = customtkinter.CTkButton(screen, text='6', command=lambda: click(6), font=('Arial', 30))
    btn6.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

    btnsub = customtkinter.CTkButton(screen, text='-', command=lambda: click('-'), font=('Arial', 30))
    btnsub.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

    # Row 3
    btn1 = customtkinter.CTkButton(screen, text='1', command=lambda: click(1), font=('Arial', 30))
    btn1.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    btn2 = customtkinter.CTkButton(screen, text='2', command=lambda: click(2), font=('Arial', 30))
    btn2.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

    btn3 = customtkinter.CTkButton(screen, text='3', command=lambda: click(3), font=('Arial', 30))
    btn3.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

    btnmulti = customtkinter.CTkButton(screen, text='*', command=lambda: click('*'), font=('Arial', 30))
    btnmulti.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

    # Row 4
    btn0 = customtkinter.CTkButton(screen, text='0', command=lambda: click(0), font=('Arial', 30))
    btn0.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

    btnclear = customtkinter.CTkButton(screen, text='C', command=clear, font=('Arial', 30))
    btnclear.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

    btnequal = customtkinter.CTkButton(screen, text='=', command=equal, font=('Arial', 30))
    btnequal.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

    btndiv = customtkinter.CTkButton(screen, text='/', command=lambda: click('/'), font=('Arial', 30))
    btndiv.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

    for i in range(5):
        screen.rowconfigure(i, weight=1)
    for j in range(4):
        screen.columnconfigure(j, weight=1)

    screen.mainloop()
    
def open_Marks():
    userTheme = user_theme
    new_appearance_mode = new_theme_mode
    
    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    def change_appearance_mode_event(self, theme_mode: str):
        customtkinter.set_appearance_mode(theme_mode)

    w = customtkinter.CTk()   
    customtkinter.set_appearance_mode(userTheme)
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

def open_Chart():
    def generate_chart():
        names = []
        chart_values = []
        for row in table.get_children():
            item = table.item(row) #Set the rows to the table
            row_values = item['values'] #row values
            names.append(row_values[0]) #setting row values
            chart_values.append(float(row_values[1])) # typecasting row values

        # Generate the chart
        x = range(len(names)) 
        y = chart_values
        plt.bar(x, y)
        plt.xticks(x, names)  # Set the x-axis labels
        plt.show()  

    def add_data():
        name = name_entry.get()
        value = value_entry.get()

        table.insert('', tk.END, values=(name, value))

        name_entry.delete(0, tk.END)
        value_entry.delete(0, tk.END)
        
    def toggle_theme():
        current_theme = sv_ttk.get_theme()
        if current_theme == "light":
            sv_ttk.set_theme("dark")
        else:
            sv_ttk.set_theme("light")

    window = tk.Tk()
    window.title("Study Buddy • Chart")
    sv_ttk.set_theme("light")
    window.resizable(False, False)
    window.iconbitmap('icon.ico')
    window.geometry('450x620')

    table_frame = ttk.Frame(window)
    table_frame.pack(pady=10)

    table_columns = ('Name', 'Value')
    table = ttk.Treeview(table_frame, columns=table_columns, show='headings')
    for column in table_columns:
        table.heading(column, text=column)
    table.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    input_frame = ttk.Frame(window)
    input_frame.pack()

    name_label = ttk.Label(input_frame, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(input_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    value_label = ttk.Label(input_frame, text="Value:")
    value_label.grid(row=1, column=0, padx=5, pady=5)
    value_entry = ttk.Entry(input_frame)
    value_entry.grid(row=1, column=1, padx=5, pady=5)

    add_button = ttk.Button(input_frame, text="Add Data", command=add_data)
    add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    generate_button = ttk.Button(window, text="Generate Chart", command=generate_chart)
    generate_button.pack(pady=10)

    window.mainloop()

def open_Help():
    userTheme = user_theme
    new_appearance_mode = new_theme_mode
    
    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    def change_appearance_mode_event(root, theme_mode: str):
        customtkinter.set_appearance_mode(theme_mode)

    def change_scaling_event(root, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def center_window(w):
        w.update_idletasks()
        width = w.winfo_width()
        height = w.winfo_height()
        x_offset = math.floor((w.winfo_screenwidth() - width) / 2)
        y_offset = math.floor((w.winfo_screenheight() - height) / 2)
        w.geometry(f"+{x_offset}+{y_offset}")

    customtkinter.set_appearance_mode(userTheme)
    customtkinter.set_default_color_theme(user_color)

    max_paragraphs = 2

    root = customtkinter.CTk()
    root.geometry(f"{1100}x{580}")
    root.title('Study Buddy • Help Desk')
    root.iconbitmap('icon.ico')

    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure((2, 3, 4), weight=0)
    root.grid_rowconfigure((0, 1, 2), weight=1)
    
    root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0, height=700)
    root.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
    root.sidebar_frame.grid_rowconfigure(6, weight=1)
    root.navigation_frame_label = customtkinter.CTkLabel(root.sidebar_frame, text="",image=None ,
                                                                compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
    root.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    # Set uniform padding between buttons
    root.sidebar_frame.grid_rowconfigure((10, 6), weight=0)
    root.sidebar_frame.grid_rowconfigure(10, weight=1)

    root.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(root.sidebar_frame, values=["System", "Light", "Dark"],
                                                                command=lambda mode: change_appearance_mode_event(root, mode))
    root.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
    root.scaling_optionemenu = customtkinter.CTkOptionMenu(root.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                                command=lambda mode: change_scaling_event(root, mode))
    root.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))

    def send(event=None):
        send = "You -> " + e.get()
        txt.insert(END, send + "\n")  # Add a newline after the user's message
        user = e.get().lower()
        e.delete(0, 'end')
            
        if user == "help":
            txt.insert(END,"Bot -> HELP MENU: `help commands`, `help utility`, `help run` or type (commandName) - help to get more info\n\n")
        
        elif user == "help commands" or user == "commands" or user == "command help":
            txt.insert(END,"Bot -> COMMAND HELP MENU: (syntax: command + commandName) `Time table` `Study timer`, `Graph plotter`, `Marks calculator`, `Study notes`, `webview`, `bard`, `version`\n\n")
            
        elif user == "help utility":
            txt.insert(END,"Bot -> UTILITY HELP MENU: Utilities present in the application:\n1.Time Table\n2.Study Timer\n3.Graph Plotter\n4.Marks Calculator\n5.Calculator\n6.Study Notes\n7.Webview\n")
        
        #command section
        elif user == "command time table":
            txt.insert(END,"Bot -> The time table is present in the main menu. There are 2 slots given to enter the activity and the time. The user can then add the desired slot using the 'Add Slot' button.\n\n")

        elif user == "command study timer":
            txt.insert(END,"Bot -> The study timer is present in the main menu. The user can enter the amount of time (in minutes). The application then sends a notification when the timer is over.\n\n")
        
        elif user == "command graph plotter":
            txt.insert(END,"Bot -> The Graph plotter applet can be opened using a button present in the main menu. Once opened the user can enter the name and the value in 2 seperate table slots. The name shows on the x axis of the graph and the value shows on the y axis of the graph.\n\n")
        
        elif user == "command marks calculator":
            txt.insert(END,"Bot -> The Marks calculator applet can be opened using a button present in the main menu. Once opened the user can enter marks for 5 total subjects and the total marks and calculate their percentage.\n\n")
        
        elif user == "command calculator":
            txt.insert(END,"Bot -> The Calculator applet can be opened using a button present in the main menu.\n\n")
            
        elif user == "command study notes":
            txt.insert(END,"Bot -> The Study notes section is present in the main menu. The user can type notes and store it as a txt file which later can be edited.\n\n")
        
        elif user == "command webview":
            txt.insert(END,"Bot -> This can be opened using a button in the main menu. After opened the student can enter a question in the prompt box and get the web response in the webview frame.\n\n")        
        
        elif user == "command bard":
            txt.insert(END,"Bot -> Bard AI can be launched from anywhere within the application. If the student has some doubt he/she can ask ai for help.\n\n")
        
        elif user == "command version" or user == "version" or user == "ver":
            txt.insert(END,"Bot -> Version Study Buddy 3.1.0\n\n")
        
        #main sections  
        elif user == "(help utility) - help":
            txt.insert(END,"Bot -> UTILITY HELP MENU - Shows all the available utility present in the Study Buddy application. Commands from the `help command` menu can be used to further explain each and every utility. \n\n")
        
        elif user == "(help commands) - help":
            txt.insert(END,"Bot -> COMMAND HELP MENU - Shows all the available commands of the bot. Commands range from many aspects. Commands can be entered through the entry to get an accurate response.\n\n")
            
        elif user == "help run":
            txt.insert(END,"Bot -> RUN HELP MENU - Shows all the possible run commands with the bot:\n1. run calculator\n2.run planner\n3.run timer\n4.run notes\n5.run marks calculator\n6.run graph plotter\n7.run webview\n8.run Bard\n\n")
        
        elif user == "run calculator":
            open_Calc()
            txt.insert(END,"\n")
        
        elif user == "run planner":
            open_Time()
            txt.insert(END,"\n")
        
        elif user == "run graph plotter":
            open_Chart()
            txt.insert(END,"\n")
        
        elif user == "run marks calculator":
            open_Marks()
            txt.insert(END,"\n")
            
        elif user == "run notes":
            open_Notes()
            txt.insert(END,"\n")
        
        elif user == "run timer":
            open_Timer()
            txt.insert(END,"\n")
            
        elif user == "run webview":
            open_web()
            txt.insert(END,"\n")
        
        elif user == "run bard":
            open_bard()
            txt.insert(END,"\n")

        # ELSE
        else:
            txt.insert(END, "Invalid Input", "\n\n")
        
    txt = customtkinter.CTkTextbox(root, width=500, height=500, font=('System', 20))
    txt.grid(row=0, column=1,columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
    txt.insert(1.0, "Bot -> HELP MENU: `help commands`, `help utility`, `help run` or type (commandName) - help to get more information about it.\n\n")
    txt.grid_rowconfigure(0, weight=1)
    txt.grid_columnconfigure(0, weight=1)

    e = customtkinter.CTkEntry(root, placeholder_text='Type a prompt:')
    e.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
    e.bind("<Return>", send)

    main_button_1 = customtkinter.CTkButton(master=root,text='Send', border_width=1, command=send)
    main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    root.mainloop()

def open_Timer():
    userTheme = user_theme
    new_appearance_mode = new_theme_mode

    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    def change_appearance_mode_event(self, theme_mode: str):
        customtkinter.set_appearance_mode(theme_mode)
        
    def start_timer():
        try:
            minutes = int(entry.get())
            seconds = minutes * 60

            timer_thread = threading.Thread(target=timer_countdown, args=(seconds,))
            timer_thread.start()

        except ValueError:
            notification.notify(
                title="Invalid Input",
                message="Please enter a valid number of minutes.",
                timeout=5  # Display notification for 5 seconds
            )
            

    def printf():
        print("Hello World")

    # Define the function to handle timer countdown and show notification
    def timer_countdown(seconds):
        def show_notification():
            notification.notify(
                title="Study Timer",
                message="Timer has ended!",
                timeout=10,
                app_icon='icon.ico',
            )

        def update_stopwatch(remaining_seconds):
            minutes, secs = divmod(remaining_seconds, 60)
            stopwatch_label.configure(text=f"{minutes:02d}:{secs:02d}")
            if remaining_seconds > 0:
                stopwatch_label.after(1000, update_stopwatch, remaining_seconds - 1)
            else:
                show_notification()

        update_stopwatch(seconds)

    # Create the GUI window
    window = customtkinter.CTk()
    window.title("Study Buddy • Timer")
    window.iconbitmap('icon.ico')
    window.resizable(False, False)
    window.attributes("-topmost", True)

    customtkinter.set_appearance_mode(userTheme)
    customtkinter.set_default_color_theme(user_color)

    entry = customtkinter.CTkEntry(window)
    entry.grid(row=0, column=0, padx=10, pady=10)

    start_button = customtkinter.CTkButton(window, text="Start", command=start_timer)
    start_button.grid(row=1, column=0, padx=10, pady=10)

    stopwatch_label = customtkinter.CTkLabel(window, font=customtkinter.CTkFont(size=40), text="00:00")
    stopwatch_label.grid(row=2, column=0, padx=10, pady=10)

    # Run the GUI main loop
    window.mainloop()

def open_Time():
    def change_scaling_event(root, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def center_window(w):
        w.update_idletasks()
        width = w.winfo_width()
        height = w.winfo_height()
        x_offset = math.floor((w.winfo_screenwidth() - width) / 2)
        y_offset = math.floor((w.winfo_screenheight() - height) / 2)
        w.geometry(f"+{x_offset}+{y_offset}")
        
    user_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
    directory_path = f"{user_path}/{signed_in_user}"

    if os.path.isdir(directory_path):
        print("Exists")
    else:
        os.makedirs(directory_path, exist_ok=True)

    def save_timetable():
        timetable_data = []
        for i in range(1, num_rows):
            row_data = [entry.get() for entry in timetable_entries[i]]
            timetable_data.append(row_data)
            
        dialog = customtkinter.CTkInputDialog(text="Enter file name:", title="Save as")
        dialog_result = dialog.get_input()  # Capture the input immediately
        
        if dialog_result is None or dialog_result.strip() == "":
            notification.notify(
                app_icon="icon.ico",
                title="Invalid File Name",
                message="Please check the file name",
                timeout=5
            )
            return  # Exit the function if input is invalid
        
        # Save the timetable data as JSON
        with open(f"{directory_path}/{dialog_result}.json", "w") as file:
            json.dump(timetable_data, file)

    def open_timetable():
        dialog = customtkinter.CTkInputDialog(text="Enter file name:", title="Open File")
        dialog_result = dialog.get_input()  # Capture the input immediately
        
        if dialog_result is None or dialog_result.strip() == "":
            notification.notify(
                app_icon="icon.ico",
                title="Invalid File Name",
                message="Please check the file name",
                timeout=5
            )
            return  # Exit the function if input is invalid
        
        # Read the timetable data from the JSON file
        try:
            with open(f"{directory_path}/{dialog_result}.json", "r") as file:
                timetable_data = json.load(file)
        except FileNotFoundError:
            notification.notify(
                app_icon="icon.ico",
                title="File Not Found",
                message="The specified file does not exist",
                timeout=5
            )
            return  # Exit the function if file is not found
        
        # Update the timetable entries with the loaded data
        for i in range(1, num_rows):
            for j in range(num_columns):
                entry = timetable_entries[i][j]
                entry.delete(0, "end")
                entry.insert(0, timetable_data[i-1][j])

    userTheme = user_theme
    new_appearance_mode = new_theme_mode

    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    customtkinter.set_appearance_mode(userTheme)
    customtkinter.set_default_color_theme(user_color)

    root = customtkinter.CTkToplevel()
    root.geometry("750x580")
    root.title(f'Study Buddy • {signed_in_user}')
    root.resizable(False, False)
    
    root.lift()
    root.focus()
    root.focus_force()
    root.attributes("-topmost", True) 
    root.after(500, lambda: root.attributes("-topmost", False))
    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
    root.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(70,70))
    
    root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0, height=700)
    root.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
    root.sidebar_frame.grid_rowconfigure(6, weight=1)
    root.navigation_frame_label = customtkinter.CTkLabel(root.sidebar_frame, text="", image=root.logo_image,
                                                                compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
    root.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)


    # Set uniform padding between buttons
    root.sidebar_frame.grid_rowconfigure((6), weight=0)
    root.sidebar_frame.grid_rowconfigure((1,2,3,4,5,7,10), weight=0)

    root.table_frame = customtkinter.CTkFrame(root)
    root.table_frame.grid(row=0, column=1, rowspan=8, columnspan=3, padx=20, pady=20, sticky="nsew")

    # Create a grid of entry widgets for the table
    table_data = [
        ["Topic", "Day", "Time"],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
    ]

    num_rows = len(table_data)
    num_columns = len(table_data[0])

    timetable_entries = []
    for i in range(num_rows):
        row_entries = []
        for j in range(num_columns):
            entry = customtkinter.CTkEntry(root.table_frame)
            entry.insert(0, table_data[i][j])
            entry.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
            
            entry.grid_configure(ipadx=10, ipady=3)
            
            # Disable the "Name", "Age", and "Gender" entries
            if i == 0:
                entry.configure(state="disabled")
            
            # Set placeholder text for the entries
            if i == 0:
                entry.configure(placeholder_text=table_data[i][j], fg_color='#4d4d4e', text_color='white')
                
            row_entries.append(entry)
        
        timetable_entries.append(row_entries)

    root.save_button = customtkinter.CTkButton(master=root, text='Save Timetable', border_width=1, command=save_timetable)
    root.save_button.grid(row=9, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew", columnspan='1')

    root.open_button = customtkinter.CTkButton(master=root, text='Open Timetable', border_width=1, command=open_timetable)
    root.open_button.grid(row=9, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
    
    root.mainloop()

def open_Notes():
    new_appearance_mode = new_theme_mode
    userTheme = user_theme
    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode
        
    def change_appearance_mode_event(self, theme_mode: str):
        customtkinter.set_appearance_mode(theme_mode)
        
    def change_scaling_event(root, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    def center_window(w):
        w.update_idletasks()
        width = w.winfo_width()
        height = w.winfo_height()
        x_offset = math.floor((w.winfo_screenwidth() - width) / 2)
        y_offset = math.floor((w.winfo_screenheight() - height) / 2)
        w.geometry(f"+{x_offset}+{y_offset}")

    user_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
    directory_path = f"{user_path}/{signed_in_user}"

    def save_notes():
        text = root.textbox.get("1.0", "end-1c")  # Get the text from the textbox

        # Save the text to a file
        dialog = customtkinter.CTkInputDialog(text="Save file as:", title="Save File")
        dialog_result = dialog.get_input()
        if dialog_result:
            with open(f"{directory_path}/{dialog_result}.txt", "w") as file:
                file.write(text)
        else:
            notification.notify(
                app_icon="icon.ico",
                title="Invalid File Name",
                message="Please check the file name",
                timeout=5
            )

    def open_notes():
        # Open the text file
        dialog = customtkinter.CTkInputDialog(text="Enter file name:", title="Open File")
        dialog_result = dialog.get_input()
        if dialog_result:
            try:
                with open(f"{directory_path}/{dialog_result}.txt", "r") as file:
                    text = file.read()
                # Clear the textbox and insert the text from the file
                root.textbox.delete("1.0", "end")
                root.textbox.insert("1.0", text)
            except FileNotFoundError:
                notification.notify(
                    app_icon="icon.ico",
                    title="File Not Found",
                    message="Please check the file name",
                    timeout=5
                )
        else:
            notification.notify(
                app_icon="icon.ico",
                title="Invalid File Name",
                message="Please check the file name",
                timeout=5
            )

    customtkinter.set_appearance_mode(userTheme)
    customtkinter.set_default_color_theme(user_color)

    root = customtkinter.CTkToplevel()
    root.geometry(f"{1100}x{580}")
    root.title('Study Buddy • Notes')
    root.iconbitmap('icon.ico')

    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure((2, 3), weight=0)
    root.grid_rowconfigure((0, 1, 2, 4), weight=1)
    
    root.lift()
    root.focus()
    root.focus_force()
    root.attributes("-topmost", True) 
    root.after(100, lambda: root.attributes("-topmost", False))

    if os.path.isdir(directory_path):
        print("Exists")
    else:
        os.makedirs(directory_path, exist_ok=True)
        
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images", "logo.png")
    root.logo_image = customtkinter.CTkImage(Image.open(image_path), size=(70,70))

    root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0, height=700)
    root.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
    root.sidebar_frame.grid_rowconfigure(6, weight=1)
    root.navigation_frame_label = customtkinter.CTkLabel(root.sidebar_frame, text="",
                                                                compound="left", font=customtkinter.CTkFont(size=20, weight="bold"), image=root.logo_image)
    root.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    # Set uniform padding between buttons
    root.sidebar_frame.grid_rowconfigure((10, 6), weight=0)
    root.sidebar_frame.grid_rowconfigure((10,11), weight=1)

    # create main entry and buttons
    root.entry = customtkinter.CTkEntry(root, placeholder_text='Click this button to save your notes: ')
    root.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

    root.main_button_1 = customtkinter.CTkButton(master=root, text='Save Notes', border_width=1, command=save_notes)
    root.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    root.main_button_2 = customtkinter.CTkButton(master=root, text='Open Notes', border_width=1, command=open_notes)
    root.main_button_2.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    root.textbox = customtkinter.CTkTextbox(root, width=500, height=500, font=customtkinter.CTkFont(size=15))
    # Increase the height to make the textbox bigger
    root.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
    root.textbox.grid_rowconfigure(0, weight=1)  # Allow the textbox to expand vertically
    root.textbox.grid_columnconfigure(0, weight=1)

    # default values:

    root.entry.configure(state='disabled')

    root.mainloop()

def open_web():
    webview.create_window("Study Buddy • Webview", "https://search.brave.com/", width=1100, height=780)
    webview.start()

def open_bard():
    username = signed_in_user
    client = genai.Client(api_key="AIzaSyCc39qw8F10MxtYrtqlIaGOjY3JjWCtd-M")

    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    userTheme = user_theme
    new_appearance_mode = new_theme_mode

    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    customtkinter.set_appearance_mode(userTheme)
    customtkinter.set_default_color_theme(user_color)

    root = customtkinter.CTkToplevel()
    root.geometry("1100x580")
    root.minsize(1100, 580)
    root.title("Study Buddy • Quill AI")
    
    root.lift()
    root.focus()
    root.focus_force()
    root.attributes("-topmost", True) 
    root.after(100, lambda: root.attributes("-topmost", False))
    
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images", "logo.png")
    root.logo_image = customtkinter.CTkImage(Image.open(image_path), size=(70,70))

    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure((2, 3, 4), weight=0)
    root.grid_rowconfigure((0, 1, 2), weight=1)

    root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0, height=700)
    root.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
    root.sidebar_frame.grid_rowconfigure(6, weight=1)

    root.navigation_frame_label = customtkinter.CTkLabel(
        root.sidebar_frame,
        text="",
        image=root.logo_image,
        compound="left",
        font=customtkinter.CTkFont(size=20, weight="bold")
    )
    root.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    root.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
        root.sidebar_frame,
        values=["System", "Light", "Dark"],
        command=lambda mode: change_appearance_mode_event(root, mode)
    )
    root.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))

    root.scaling_optionemenu = customtkinter.CTkOptionMenu(
        root.sidebar_frame,
        values=["80%", "90%", "100%", "110%", "120%"],
        command=lambda mode: change_scaling_event(mode)
    )
    root.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))

    txt = customtkinter.CTkTextbox(root, width=500, height=500, font=('Inter', 20))
    txt.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew", ipadx=20, ipady=20)

    def send(event=None):
        user_input = e.get()
        if user_input.strip().lower() == "clear":
            txt.delete("0.0", "end")
        else:
            txt.insert("end", f"{username} -> {user_input}\n")
            response = client.models.generate_content_stream(
                model="gemini-2.0-flash",
                contents=[user_input]
            )
            for chunk in response:
                txt.insert("end", chunk.text or "")
            txt.insert("end", "\n\n")
        e.delete(0, 'end')

    e = customtkinter.CTkEntry(root, placeholder_text='Type a prompt:')
    e.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
    e.bind("<Return>", send)

    send_button = customtkinter.CTkButton(root, text='Send', border_width=1, command=send)
    send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    root.mainloop()

def open_Sticky():
    def createWindow():
        open_Sticky()
        
    w=customtkinter.CTk()
    w.geometry("240x228")
    w.title("")
    w.iconbitmap("icon.ico")

    w.resizable(False, False)
    if(user_color == "green"):           
        w.configure(fg_color=("#5AD75D"))
        userChoice = "#5AD75D"
    elif(user_color == "blue"):
        w.configure(fg_color=("#5AA2D7"))
        userChoice="#5AA2D7"
    else:
        w.configure(fg_color=("#5A87D7"))
        userChoice="#5A87D7"
    w.attributes("-topmost", True)
    
    textbox = customtkinter.CTkTextbox(w, height=200, width=230, fg_color=userChoice, font=customtkinter.CTkFont(family="Consolas", size=17), text_color="black")
    textbox.grid()
    button = customtkinter.CTkButton(w, fg_color=("#F5F5DC", "#212121"), corner_radius=5, width=250, text="+", text_color=("black", "white"), image=None, hover_color=("#DCDCC6", "#1a1a1a"), command=createWindow)
    button.grid(row=10, columnspan=10)
    
    w.mainloop()

def open_Profile():
    userTheme = user_theme
    new_appearance_mode = new_theme_mode

    if userTheme != new_appearance_mode:
        userTheme = new_appearance_mode

    customtkinter.set_appearance_mode(userTheme)
    customtkinter.set_default_color_theme(user_color)
    
    usercolor = user_color
    app = customtkinter.CTkToplevel()
    app.title(f"Studybuddy • Profile")
    app.geometry("420x420")
    app.iconbitmap("icon.ico")
    app.resizable(False, False)
    
    app.lift()
    app.focus()
    app.focus_force()
    app.attributes("-topmost", True) 
    app.after(200, lambda: app.attributes("-topmost", False))

    def create_file(file_path, content=""):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"File '{file_path}' created successfully.")
        except Exception as e:
            print(f"Error creating file '{file_path}': {e}")
            
    def editPassword():
        dialog = customtkinter.CTkInputDialog(text="Type in your password:", title="Edit Password")
        newPassword = dialog.get_input()
        
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
            
        mySql = f"UPDATE users set password = '{newPassword}' where username='{signed_in_user}'"
        cursor.execute(f'{mySql}')

        # Commit the changes
        connection.commit()
                
        # Close the connection
        connection.close()
            
        file_path = "ProfileChanges.txt"
        file_content = f"Password changed to {newPassword}"

        create_file(file_path, file_content)
            
        time.sleep(1.5)   
        app.destroy()

    def editUserName():
        dialog = customtkinter.CTkInputDialog(text="Type in your username:", title="Edit Username")
        newUserName = dialog.get_input()
        count = int(0)
        
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT username FROM users")

        # Fetch all results
        rows = cursor.fetchall()

        for row in rows:
            if(row[0] == newUserName):
                count = count + 1
                
        if(count>=1):
            notification.notify(
                title="Username already exists.",
                message="Please enter a valid username.",
                timeout=5  # Display notification for 5 seconds
            )
            connection.close()
        else:              
            mySql = f"UPDATE users set username = '{newUserName}' where username='{signed_in_user}'"
            cursor.execute(f'{mySql}')

            # Commit the changes
            connection.commit()
                
            # Close the connection
            connection.close()
            users_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
            old_path = os.path.join(users_dir, signed_in_user)
            new_path = os.path.join(users_dir, newUserName)
            
            os.rename(old_path, new_path)
            print(f"Folder '{old_path}' successfully renamed to '{new_path}'.")
            
            file_path = "ProfileChanges.txt"
            file_content = f"Username changed from {signed_in_user} to {newUserName}"

            create_file(file_path, file_content)
            
            time.sleep(1.5)
            
            app.destroy()
            

        
    try:
        profile_image = Image.open("profile_pic.png")
        profile_image = profile_image.resize((50, 50))
        profile_photo = ImageTk.PhotoImage(profile_image)
        profile_label = customtkinter.CTkLabel(app, image=profile_photo, text="")
        profile_label.image = profile_photo
        profile_label.pack(pady=(20, 0))
    except FileNotFoundError:
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
        if(usercolor == "blue"):
            profile_image = Image.open(os.path.join(image_path, "profilePlaceholder-Blue.png"))
        elif(usercolor == "dark-blue"):
            profile_image = Image.open(os.path.join(image_path, "profilePlaceholder-DBlue.png"))
        else:
            profile_image = Image.open(os.path.join(image_path, "profilePlaceholder-Green.png"))
        profile_image = profile_image.resize((120, 120))
        profile_photo = ImageTk.PhotoImage(profile_image)
        profile_label = customtkinter.CTkLabel(app, image=profile_photo, text="")
        profile_label.image = profile_photo
        profile_label.pack(pady=(20, 0))
        
    ctkFont = customtkinter.CTkFont(
        family="Inter",
        size=20
    )
        
    usernameLabel = customtkinter.CTkLabel(app, text=signed_in_user, font=ctkFont)
    usernameLabel.pack(pady=20)

    #Edit Username
    frame = customtkinter.CTkFrame(app, width=300, height=50, border_width=1, border_color="#1f1f1f",)
    frame.pack(pady=5)

    text_label = customtkinter.CTkLabel(frame, text=f"Username: {signed_in_user}", anchor="w") 
    text_label.place(x=10, rely=0.5, anchor="w")  

    button = customtkinter.CTkButton(frame, text="Edit", width=60, height=30, command=editUserName) 
    button.place(relx=0.95, rely=0.5, anchor="e") 

    #Edit Password
    frame = customtkinter.CTkFrame(app, width=300, height=50, border_width=1, border_color="#1f1f1f",)
    frame.pack(pady=5)

    text_label = customtkinter.CTkLabel(frame, text=f"Edit Password", anchor="w") 
    text_label.place(x=10, rely=0.5, anchor="w")  

    button = customtkinter.CTkButton(frame, text="Edit", width=60, height=30, command=editPassword) 
    button.place(relx=0.95, rely=0.5, anchor="e") 

    frame = customtkinter.CTkFrame(app, width=300, height=50, border_width=1, border_color="#1f1f1f",)
    frame.pack(pady=5)

    text_label = customtkinter.CTkLabel(frame, text="StudyBuddy Version: ", anchor="w") 
    text_label.place(x=10, rely=0.5, anchor="w")  

    buttonVer = customtkinter.CTkButton(frame, text="6.0", width=60, height=30, text_color_disabled="white")
    buttonVer.place(relx=0.95, rely=0.5, anchor="e") 

    buttonVer.configure(state="disabled")

    app.mainloop()
    
def check_file_exists(file_name, directory="."):
    file_path = os.path.join(directory, file_name) 
    return os.path.isfile(file_path)
    
def checkProfileChanges(event=None):
    file_to_check = "ProfileChanges.txt"
    if check_file_exists(file_to_check):
        print(f"File '{file_to_check}' exists.")
        os.remove(file_to_check)
        reopen_signInPage(self)
    else:
        print(f"File '{file_to_check}' does not exist.")

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
    subprocess.run(["python", "main.py"])
    self.withdraw()
         
def close_current_window(): 
    self.destroy()  
    open_home_window() 
        
def userLogout():
    logSignInSignOutTime(False, signed_in_user)
    self.after(1000, close_current_window)
    
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

#ApplyMica(HWND=parent_hwnd, Theme=mode, Style=style, OnThemeChange=callbackFunction)
self.title(f'Study Buddy - Hello {signed_in_user}')
self.iconbitmap('icon.ico')
self.bind("<FocusIn>", checkProfileChanges)

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
self.profilePlaceholder = customtkinter.CTkImage(Image.open(os.path.join(image_path, "profilePlaceholder.png")), size=(22,22))

self.plusIcon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plus.png")), size=(15,15))

self.btnCalc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calc.png")), size=(32,32))
self.btnPlanner = customtkinter.CTkImage(Image.open(os.path.join(image_path, "planner.png")), size=(32,32))
self.btnNotes = customtkinter.CTkImage(Image.open(os.path.join(image_path, "notes.png")), size=(32,32))
self.btnTimer = customtkinter.CTkImage(Image.open(os.path.join(image_path, "timer.png")), size=(32,32))
self.btnGraph = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plotter.png")), size=(32,32))
self.btnMarks = customtkinter.CTkImage(Image.open(os.path.join(image_path, "marks.png")), size=(32,32))
self.btnBard = customtkinter.CTkImage(Image.open(os.path.join(image_path, "quill.png")), size=(32,32))
self.btnWeb = customtkinter.CTkImage(Image.open(os.path.join(image_path, "webview.png")), size=(32,32))
self.btnSticky = customtkinter.CTkImage(Image.open(os.path.join(image_path, "sticky.png")), size=(32,32))

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

self.btnLogout = customtkinter.CTkButton(self.sidebar_frame, image=self.logout, text="", compound='left', fg_color="#cf352e", hover_color="#B02B25", command=userLogout, width=60)
self.btnLogout.grid(row=14, column=0, pady=10, padx=(70, 5)) 

self.newButton = customtkinter.CTkButton(self.sidebar_frame, text="", image=self.profilePlaceholder, width=60, command=open_Profile)  
self.newButton.grid(row=14, column=0, pady=10, padx=(5, 70)) 

self.sidebar_frame.columnconfigure(0, weight=0)
self.sidebar_frame.columnconfigure(1, weight=0)

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