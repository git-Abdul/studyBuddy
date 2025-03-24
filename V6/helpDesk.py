import customtkinter
import subprocess
import requests
from customtkinter import *
import customtkinter
import os
from PIL import Image
import math

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

signed_in_user = sys.argv[1]
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

customtkinter.set_appearance_mode(user_theme)
customtkinter.set_default_color_theme(user_color)

max_paragraphs = 2

self = customtkinter.CTk()
self.geometry(f"{1100}x{580}")
self.title('Study Buddy • Help Desk')
self.state('zoomed')
self.iconbitmap('icon.ico')


self.grid_columnconfigure(1, weight=1)
self.grid_columnconfigure((2, 3, 4), weight=0)
self.grid_rowconfigure((0, 1, 2), weight=1)

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
self.navigation_frame_label = customtkinter.CTkLabel(self.sidebar_frame, text=" Study Buddy", image=self.logo_image,
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
      
txt = customtkinter.CTkTextbox(self, width=500, height=500, font=('System', 20))
txt.grid(row=0, column=1,columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
txt.insert(1.0, "Bot -> HELP MENU: `help commands`, `help utility`, `help run` or type (commandName) - help to get more information about it.\n\n")
txt.grid_rowconfigure(0, weight=1)
txt.grid_columnconfigure(0, weight=1)
txt.configure(state="disabled")

e = customtkinter.CTkEntry(self, placeholder_text='Type a prompt:')
e.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
e.bind("<Return>", send)

main_button_1 = customtkinter.CTkButton(master=self,text='Send', border_width=1, command=send)
main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

self.mainloop()
