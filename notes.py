import customtkinter
import subprocess
import math
import os
from PIL import Image
import tkinter as tk
import sys
from plyer import notification

# Making the text crisp
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

signed_in_user = sys.argv[1]
user_color = sys.argv[2]
user_theme = sys.argv[3] 

# functions=====================================================================

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
    subprocess.run(["python", "Calculator.py", signed_in_user, user_color, user_theme, new_theme_mode])

def open_Marks():
    subprocess.run(["python", "Marks.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Chart():
    subprocess.run(["python", "Chart.py", signed_in_user, user_color, user_theme, new_theme_mode])

def open_Help():
    subprocess.run(['python', 'helpDesk.py', signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Time():
    subprocess.run(['python', 'planner.py', signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_Timer():
    subprocess.run(['python', 'timer.py', signed_in_user, user_color, user_theme, new_theme_mode])

def open_Notes():
    subprocess.run(["python", "notes.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_bard():
    subprocess.run(["python", "quill.py", signed_in_user, user_color, user_theme, new_theme_mode])
    
def open_web():
    subprocess.run(["python", "browser.py", signed_in_user, user_color, user_theme, new_theme_mode])

user_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
directory_path = f"{user_path}/{signed_in_user}"

def save_notes():
    text = self.textbox.get("1.0", "end-1c")  # Get the text from the textbox

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
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", text)
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
        
# functions=====================================================================

customtkinter.set_appearance_mode(user_theme)  # Modes: "System" (standard), "Dark","Light"
customtkinter.set_default_color_theme(user_color)

self = customtkinter.CTk()
self.geometry(f"{1100}x{580}")
self.title('Study Buddy • Notes')
self.iconbitmap('icon.ico')

self.grid_columnconfigure(1, weight=1)
self.grid_columnconfigure((2, 3), weight=0)
self.grid_rowconfigure((0, 1, 2, 4), weight=1)

if os.path.isdir(directory_path):
    print("Exists")
else:
    os.makedirs(directory_path, exist_ok=True)

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
self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
self.sidebar_frame.grid_rowconfigure(6, weight=1)
self.navigation_frame_label = customtkinter.CTkLabel(self.sidebar_frame, text=" StudyBuddy", image=self.logo_image,
                                                            compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

# Set uniform padding between buttons
self.sidebar_frame.grid_rowconfigure((10, 6), weight=0)
self.sidebar_frame.grid_rowconfigure((10,11), weight=1)

# create main entry and buttons
self.entry = customtkinter.CTkEntry(self, placeholder_text='Click this button to save your notes: ')
self.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

self.main_button_1 = customtkinter.CTkButton(master=self, text='Save Notes', border_width=1, command=save_notes)
self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

self.main_button_2 = customtkinter.CTkButton(master=self, text='Open Notes', border_width=1, command=open_notes)
self.main_button_2.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

self.textbox = customtkinter.CTkTextbox(self, width=500, height=500, font=customtkinter.CTkFont(size=15))
# Increase the height to make the textbox bigger
self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
self.textbox.grid_rowconfigure(0, weight=1)  # Allow the textbox to expand vertically
self.textbox.grid_columnconfigure(0, weight=1)

# default values:

self.entry.configure(state='disabled')

self.mainloop()
