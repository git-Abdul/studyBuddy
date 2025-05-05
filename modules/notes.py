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

def change_appearance_mode_event(root, new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


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
        
# functions=====================================================================

customtkinter.set_appearance_mode(user_theme)  # Modes: "System" (standard), "Dark","Light"
customtkinter.set_default_color_theme(user_color)

root = customtkinter.CTk()
root.geometry(f"{1100}x{580}")
root.title('Study Buddy • Notes')
root.iconbitmap('icon.ico')

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2, 4), weight=1)

if os.path.isdir(directory_path):
    print("Exists")
else:
    os.makedirs(directory_path, exist_ok=True)

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
root.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(35, 35))
root.bard = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bard.png")), size=(20,20))
root.web = customtkinter.CTkImage(Image.open(os.path.join(image_path, "webview.png")), size=(20,20))
root.notes = customtkinter.CTkImage(Image.open(os.path.join(image_path, "notes.png")), size=(20,20))
root.timer = customtkinter.CTkImage(Image.open(os.path.join(image_path, "timer.png")), size=(20,20))
root.planner = customtkinter.CTkImage(Image.open(os.path.join(image_path, "planner.png")), size=(20,20))
root.marks = customtkinter.CTkImage(Image.open(os.path.join(image_path, "marks.png")), size=(20,20))
root.plotter = customtkinter.CTkImage(Image.open(os.path.join(image_path, "plotter.png")), size=(20,20))
root.calc = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calc.png")), size=(20,20))

root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0, height=700)
root.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
root.sidebar_frame.grid_rowconfigure(6, weight=1)
root.navigation_frame_label = customtkinter.CTkLabel(root.sidebar_frame, text=" StudyBuddy", image=root.logo_image,
                                                            compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
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
