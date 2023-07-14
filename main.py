import customtkinter
import subprocess
import math

#Making the text crisp
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

w = customtkinter.CTk()
w.geometry("500x250")
w.iconbitmap('icon.ico')
w.overrideredirect(True)
w.attributes("-topmost", True)

slider_progressbar_frame = customtkinter.CTkFrame(w, fg_color="transparent")
slider_progressbar_frame.grid(row=3, column=2, padx=(104, 100), pady=(100, 0))

logo_label = customtkinter.CTkLabel(w, text='Study Buddy', font=customtkinter.CTkFont(size=30, weight="bold"))
logo_label.grid(row=3, column=2, padx=10, pady=75)

progress_bar = customtkinter.CTkProgressBar(slider_progressbar_frame, width=300)
progress_bar.pack()

progress_bar.configure(mode='intermediate')
progress_bar.start()

def open_new_window():
    subprocess.run(["python", "home.py"])

def close_current_window():
    w.after_cancel(cancel_id)  # Cancel the scheduled closing
    w.destroy()  # Close the current window
    open_new_window()  # Open a new window
    
def center_window(w):
    w.update_idletasks()
    width = w.winfo_width()
    height = w.winfo_height()
    x_offset = math.floor((w.winfo_screenwidth() - width) / 2)
    y_offset = math.floor((w.winfo_screenheight() - height) / 2)
    w.geometry(f"+{x_offset}+{y_offset}")
    
cancel_id = w.after(5000, close_current_window)
w.after(0, lambda: center_window(w))

w.mainloop()