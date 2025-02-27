import customtkinter
import subprocess
from customtkinter import *
import customtkinter
from google import genai
import os
from PIL import Image
import math

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

username = sys.argv[1]
user_color = sys.argv[2]
user_theme = sys.argv[3]
client = genai.Client(api_key=None) 

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
    subprocess.run(["python", "Calculator.py", username, user_color, user_theme, new_theme_mode])

def open_Marks():
    subprocess.run(["python", "Marks.py", username, user_color, user_theme, new_theme_mode])
    
def open_Chart():
    subprocess.run(["python", "Chart.py", username, user_color, user_theme, new_theme_mode])

def open_Help():
    subprocess.run(['python', 'helpDesk.py', username, user_color, user_theme, new_theme_mode])
    
def open_Time():
    subprocess.run(['python', 'planner.py', username, user_color, user_theme, new_theme_mode])
    
def open_Timer():
    subprocess.run(['python', 'timer.py', username, user_color, user_theme, new_theme_mode])

def open_Notes():
    subprocess.run(["python", "notes.py", username, user_color, user_theme, new_theme_mode])
    
def open_bard():
    subprocess.run(["python", "quill.py", username, user_color, user_theme, new_theme_mode])
    
def open_web():
    subprocess.run(["python", "browser.py", username, user_color, user_theme, new_theme_mode])

customtkinter.set_appearance_mode(user_theme)
customtkinter.set_default_color_theme(user_color)

max_paragraphs = 2

self = customtkinter.CTk()
self.geometry(f"{1100}x{580}")
self.title('Study Buddy • Quill AI')
self.state('zoomed')
self.iconbitmap('icon.ico')


self.grid_columnconfigure(1, weight=1)
self.grid_columnconfigure((2, 3, 4), weight=0)
self.grid_rowconfigure((0, 1, 2), weight=1)

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(70, 70))
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
self.navigation_frame_label = customtkinter.CTkLabel(self.sidebar_frame, text="", image=self.logo_image,
                                                            compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

# Set uniform padding between buttons
self.sidebar_frame.grid_rowconfigure((10, 6), weight=0)
self.sidebar_frame.grid_rowconfigure(10, weight=1)

self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                            command=lambda mode: change_appearance_mode_event(self, mode))
self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=lambda mode: change_scaling_event(self, mode))
self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))
      
txt = customtkinter.CTkTextbox(self, width=500, height=500, font=('Inter', 20))
txt.grid(row=0, column=1,columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew", ipadx=20, ipady=20)
txt.grid_rowconfigure(0, weight=1)
txt.grid_columnconfigure(0, weight=1)

def send(event=None):
    send = f"{username} -> " + e.get()
    user = e.get().lower()
    
    if user == "clear":
        txt.delete("0.0", "end")
    else:
        txt.insert(END, send + "\n")
        response = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=[user])
        for chunk in response:
            txt.insert(END, chunk.text + "")
        txt.insert("\n\n")
    e.delete(0, 'end')

e = customtkinter.CTkEntry(self, placeholder_text='Type a prompt:')
e.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
e.bind("<Return>", send)

main_button_1 = customtkinter.CTkButton(master=self,text='Send', border_width=1, command=send)
main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

self.mainloop()
