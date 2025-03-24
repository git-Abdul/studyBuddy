from tkinter import *

class MyUI:
    def __init__(self, parent):
        parent.geometry("500x100")

        button = Button(parent, text="Sample button")
        button.pack(pady=20)

        mainmenu = Menu(parent)
        parent.config(menu=mainmenu)

        file_menu = Menu(mainmenu, tearoff=False)
        menu_1 = Menu(mainmenu, tearoff=False)
        menu_2 = Menu(mainmenu, tearoff=False)
        menu_3 = Menu(mainmenu, tearoff=False)
        menu_4 = Menu(mainmenu, tearoff=False)

        mainmenu.add_cascade(label="File", menu=file_menu)
        mainmenu.add_cascade(label="Menu 1", menu=menu_1)
        mainmenu.add_cascade(label="Menu 2", menu=menu_2)
        mainmenu.add_cascade(label="Menu 3", menu=menu_3)
        mainmenu.add_cascade(label="Menu 4", menu=menu_4)

        file_menu.add_command(label="Duplicate window", command=self.new_window)
        menu_1.add_command(label="Sub-menu 1")
        menu_2.add_command(label="Sub-menu 2")
        menu_3.add_command(label="Sub-menu 3")
        menu_4.add_command(label="Sub-menu 4")

    def new_window(self):
        win = Toplevel()
        MyUI(win)

root = Tk()
MyUI(root)
root.mainloop()