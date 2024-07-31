import customtkinter
from customtkinter import CTkToplevel
import PIL.Image
import os

class newWindow:
    def __init__(self, w):

        w.geometry("240x228")
        w.title("")
        w.iconbitmap("icon.ico")
    
        customtkinter.set_appearance_mode("System")
        a = customtkinter.get_appearance_mode()
    
        w.resizable(False, False)
        if(a == "Light"):           
            w.configure(fg_color=("#fdde6c"))
        else:
            w.configure(fg_color=("#c69f26"))
        w.attributes("-topmost", True)
    
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
        plusIcon = customtkinter.CTkImage(PIL.Image.open(os.path.join(image_path, "splus.png")), size=(15,15))
        
        textbox = customtkinter.CTkTextbox(w, height=200, width=230, fg_color=("#fdde6c", "#c69f26"), font=customtkinter.CTkFont(family="Consolas", size=17))
        textbox.grid()
        button = customtkinter.CTkButton(w, fg_color=("#F5F5DC", "#fada5f"), corner_radius=5, width=250, text=None, text_color="black", image=plusIcon, hover_color=("#E5E3A3", "#f8cf2e"), command=self.createWindow)
        button.grid(row=10, columnspan=10)
    
    def createWindow(self):
        win = CTkToplevel()
        newWindow(win)

root = customtkinter.CTk()
newWindow(root)
root.mainloop()