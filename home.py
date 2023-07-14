import customtkinter
import subprocess
import math
import os
from PIL import Image

#Making the text crisp
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

#functions================================================================================================================================

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
    
def open_Time():
    subprocess.run(['python', 'planner.py'])
    
def open_Timer():
    subprocess.run(['python', 'timer.py'])

def open_Notes():
    subprocess.run(["python", "notes.py"])
    
def open_web():
    subprocess.run(["python", "browser.py"])
    
def open_bard():
    subprocess.run(["python", "bard.py"])
    
#functions=====================================================================

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")

self = customtkinter.CTk()
self.geometry(f"{1100}x{580}")
self.title('Study Buddy • Home')
self.iconbitmap('icon.ico')
self.state('zoomed')

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

self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0, height=700)
self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
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

self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=open_Time, image=self.planner, compound="right", text='Open Planner')
self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=(10, 10))  

self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=open_Timer, image=self.timer, compound="right", text='Open Timer')
self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)  

self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, command=open_Notes, image=self.notes, compound="right", text='Open Notes')
self.sidebar_button_6.grid(row=6, column=0, padx=20, pady=10)

self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, command=open_web, image= self.web, compound="right", text='Open Webview')
self.sidebar_button_7.grid(row=7, column=0, padx=20, pady=10)

self.home_frame_button_8 = customtkinter.CTkButton(self.sidebar_frame, text="Open Bard AI", image=self.bard, compound="right", command=open_bard)
self.home_frame_button_8.grid(row=8, column=0, padx=20, pady=10)

# Set uniform padding between buttons
self.sidebar_frame.grid_rowconfigure((10, 6), weight=0)
self.sidebar_frame.grid_rowconfigure(10, weight=1)

self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
self.appearance_mode_label.grid(row=10, column=0, padx=20, pady=(10, 0))
self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"],
                                                            command=lambda mode: change_appearance_mode_event(self, mode))
self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                            command=lambda mode: change_scaling_event(self, mode))
self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))

# create main entry and button
self.entry = customtkinter.CTkEntry(self, placeholder_text='Facing any issues? Open the help desk for more information about the application!')
self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

self.main_button_1 = customtkinter.CTkButton(master=self,text='Open Help desk', border_width=1, command=open_Help)
self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

self.textbox = customtkinter.CTkTextbox(self, width=500, height=500, font=customtkinter.CTkFont(size=15))  # Increase the height to make the textbox bigger
self.textbox.grid(row=0, column=1,columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
self.textbox.grid_rowconfigure(0, weight=1)  # Allow the textbox to expand vertically
self.textbox.grid_columnconfigure(0, weight=1)

#default values: 

self.entry.configure(state='disabled')
self.textbox.insert("0.0", 'Welcome to Study Buddy!\n\nAre you tired of studying alone and looking for a reliable study partner? Look no further! Study Buddy is here to revolutionize your study experience. Our innovative app connects you with like-minded individuals who share your academic goals, creating a supportive community that motivates and inspires you to reachyour full potential.\n\nWith Study Buddy, you can:\n\nSet Goals and Track Progress: Achieve your academic targets with Study Buddy\'s goal-setting feature. Define your study objectives, track your progress, and celebrate milestones together with your study partner. Our app keeps you motivated, focused, and accountable throughout your learning journey.\n\nMaintain Privacy and Security: At Study Buddy, we prioritize your privacy and security. Our app employs robust encryption measures to safeguard your personal information and study data. You can study with confidence, knowing that your privacy is our utmost concern.\n\nDon\'t let the challenges of studying alone hold you back. Join Study Buddy today and unlock a world of collaborative learning, support, and academic success. Together, we can achieve more!\n\nStart now and embark on an exciting study journey with Study Buddy. Let\'s study smarter, together!\n\nPROJECT CREDITS: \n\n• Abdul 9B\n• Laksh 9C\n• Naman 9B\n• Kaladhar 9C')

self.mainloop()