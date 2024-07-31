from customtkinter import *
import sys

class CTkFloatingWindow(CTkToplevel):
    
    def __init__(self,
                 master=None,
                 alpha=0.99,
                 width=300,
                 height=300,
                 x=None,
                 y=None,
                 corner_radius=25,
                 border_width=1,
                 cancel_button=True,
                 **kwargs):
        
        super().__init__(takefocus=1)
        
        self.focus()
        self.master_window = master
        self.width = width
        self.height = height
        self.attributes('-alpha', 0)
        self.corner = corner_radius
        self.border = border_width
        
        if sys.platform.startswith("win"):
            self.after(100, lambda: self.overrideredirect(True))
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
        else:
            self.attributes("-type", "splash")
            self.transparent_color = '#000001'
            self.corner = 0
            self.withdraw()
             
        self.frame = CTkFrame(self, bg_color=self.transparent_color, corner_radius=self.corner, border_width=self.border, **kwargs)
        self.frame.pack(expand=True, fill="both")
        self.frame.bind("<B1-Motion>", self.move_window)
        self.frame.bind("<ButtonPress-1>", self.oldxyset)
        
        if cancel_button:
            self.button_close = CTkButton(self.frame, corner_radius=10, width=0, height=0, hover=False,
                                          text_color=self.frame._border_color, text="✕", fg_color="transparent",
                                          command=lambda: self.destroy())
            self.button_close.pack(side="top", anchor="ne", padx=7+self.border, pady=7+self.border)
            self.button_close.configure(cursor="arrow")
            
        self.resizable(width=False, height=False)
        self.transient(self.master_window)
         
        self.update_idletasks()
        
        if self.master_window is None:
            self.x = int((self.winfo_screenwidth()-self.width)/2) if x is None else x
            self.y = int((self.winfo_screenheight()-self.height)/2) if y is None else y
        else:
            self.x = int(self.master_window.winfo_width() * .5 + self.master_window.winfo_x() - .5 * self.width + 7) if x is None else x
            self.y = int(self.master_window.winfo_height() * .5 + self.master_window.winfo_y() - .5 * self.height + 20) if y is None else y
    
        self._iconify()
        self.attributes('-alpha', alpha)
        
    def popup(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self._iconify()

    def _iconify(self):
        self.deiconify()
        self.focus()
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

    def configure(self, **kwargs):
        if "width" in kwargs:
            self.width = kwargs.pop("width")
        if "height" in kwargs:
            self.width = kwargs.pop("height")
        if "alpha" in kwargs:
            self.attributes('-alpha', kwargs.pop("alpha"))
        if "x" in kwargs:
            self.x = kwargs.pop("x")
        if "y" in kwargs:
            self.y = kwargs.pop("y")
        self.frame.configure(**kwargs)
        
    def oldxyset(self, event):
        self.oldx = event.x
        self.oldy = event.y
    
    def move_window(self, event):
        self.y = event.y_root - self.oldy
        self.x = event.x_root - self.oldx
        self.geometry(f'+{self.x}+{self.y}')
        
if __name__ == "__main__":
    app = CTkFloatingWindow()
    app.mainloop()