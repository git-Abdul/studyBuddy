import customtkinter as tk
import subprocess
import customtkinter
import math
import os
from PIL import Image
import json
import sys
from plyer import notification

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

user_color = sys.argv[2]
user_theme = sys.argv[3] 

new_theme_mode = sys.argv[4]
if user_theme != new_theme_mode:
    user_theme = new_theme_mode

def change_appearance_mode_event(self, new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(self, new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

def center_window(w):
    w.update_idletasks()
    width = w.winfo_width()
    height = w.winfo_height()
    x_offset = math.floor((w.winfo_screenwidth() - width) / 2)
    y_offset = math.floor((w.winfo_screenheight() - height) / 2)
    w.geometry(f"+{x_offset}+{y_offset}")

def open_Calc():
    subprocess.run(["python", "Calculator.py"])

def open_Marks():
    subprocess.run(["python", "Marks.py"])

def open_Chart():
    subprocess.run(["python", "Chart.py"])

def open_Help():
    subprocess.run(['python', 'helpDesk.py'])
    
def open_Timer():
    subprocess.run(['python', 'timer.py'])
    
def open_Notes():
    subprocess.run(["python", "notes.py"])
    
def open_web():
    subprocess.run(["python", "browser.py"])
    
def open_bard():
    subprocess.run(["python", "bard.py"])
    
signed_in_user = sys.argv[1]
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

customtkinter.set_appearance_mode(user_theme)
customtkinter.set_default_color_theme(user_color)

self = customtkinter.CTk()
self.geometry(f"{750}x{580}")
self.title(f'Study Buddy • {signed_in_user}')
self.iconbitmap('icon.ico')
self.resizable(False, False)

self.grid_columnconfigure(1, weight=1)
self.grid_columnconfigure((2,3), weight=0)
self.grid_rowconfigure((0, 1, 2, 4), weight=1)

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(35, 35))
self.bard = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bard.png")), size=(20,20))
self.web = customtkinter.CTkImage(Image.open(os.path.join(image_path, "webview.png")), size=(20,20))
self.notes = customtkinter.CTkImage(Image.open(os.path.join(image_path, "notes.png")), size=(20,20))
self.timer = customtkinter.CTkImage(Image.open(os.path.join(image_path, "timer.png")), size=(20,20))
self.planner = customtkinter.CTkImage(Image.open(os.path.join(image_path, "planner.png")), size=(20,20))
self.marks = customtkinter.CTkImage(Image.open(os.path.join(image_path, "marks.png")), size=(20,20))
self.plotter = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plotter.png")), size=(20,20))
self.calc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calc.png")), size=(20,20))

self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0, height=700)
self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
self.sidebar_frame.grid_rowconfigure(6, weight=1)
self.navigation_frame_label = customtkinter.CTkLabel(self.sidebar_frame, text=" Study Buddy", image=self.logo_image,
                                                            compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=open_Calc, image=self.calc, compound="right", text='Open Calculator')
self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=(20, 10))

self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=open_Chart, image=self.plotter, compound='right', text='Open Graph')
self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=open_Marks, image=self.marks, compound='right', text='Open Marks Calc')
self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=open_Timer, image=self.timer, compound="right", text='Open Timer')
self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)  

self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, command=open_Notes, image=self.notes, compound="right", text='Open Notes')
self.sidebar_button_6.grid(row=6, column=0, padx=20, pady=10)

self.home_frame_button_8 = customtkinter.CTkButton(self.sidebar_frame, text="Open Bard AI", image=self.bard, compound="right", command=open_bard)
self.home_frame_button_8.grid(row=7, column=0, padx=20, pady=10)

# Set uniform padding between buttons
self.sidebar_frame.grid_rowconfigure((6), weight=0)
self.sidebar_frame.grid_rowconfigure((1,2,3,4,5,7,10), weight=0)

self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                            command=lambda mode: change_appearance_mode_event(self, mode))
self.appearance_mode_optionmenu.grid(row=9, column=0, padx=20, pady=(10, 10))
self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=lambda mode: change_scaling_event(self, mode))
self.scaling_optionmenu.grid(row=10, column=0, padx=20, pady=(10, 20))

self.table_frame = tk.CTkFrame(self)
self.table_frame.grid(row=0, column=1, rowspan=8, columnspan=3, padx=20, pady=20, sticky="nsew")

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
        entry = tk.CTkEntry(self.table_frame)
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

self.save_button = customtkinter.CTkButton(master=self, text='Save Timetable', border_width=1, command=save_timetable)
self.save_button.grid(row=9, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew", columnspan='1')

self.open_button = customtkinter.CTkButton(master=self, text='Open Timetable', border_width=1, command=open_timetable)
self.open_button.grid(row=9, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")

self.mainloop()
