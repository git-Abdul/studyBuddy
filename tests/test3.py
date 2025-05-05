import customtkinter
class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("tab 1")
        self.add("tab 2")

        # add widgets on tabs
        segemented_button = customtkinter.CTkSegmentedButton(master=self.tab("tab 1"), values=["Value 1", "Value 2", "Value 3"])
        segemented_button.set("Value 1")
        segemented_button.pack()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.mainloop()