import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import sv_ttk

# Making the text crisp
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

def generate_chart():
    names = []
    chart_values = []
    for row in table.get_children():
        item = table.item(row) #Set the rows to the table
        row_values = item['values'] #row values
        names.append(row_values[0]) #setting row values
        chart_values.append(float(row_values[1])) # typecasting row values

    # Generate the chart
    x = range(len(names)) 
    y = chart_values
    plt.bar(x, y)
    plt.xticks(x, names)  # Set the x-axis labels
    plt.show()  

def add_data():
    name = name_entry.get()
    value = value_entry.get()

    table.insert('', tk.END, values=(name, value))

    name_entry.delete(0, tk.END)
    value_entry.delete(0, tk.END)
    
def toggle_theme():
    current_theme = sv_ttk.get_theme()
    if current_theme == "light":
        sv_ttk.set_theme("dark")
    else:
        sv_ttk.set_theme("light")

window = tk.Tk()
window.title("Study Buddy • Chart")
sv_ttk.set_theme("light")
window.resizable(False, False)
window.iconbitmap('icon.ico')
window.geometry('450x620')

table_frame = ttk.Frame(window)
table_frame.pack(pady=10)

table_columns = ('Name', 'Value')
table = ttk.Treeview(table_frame, columns=table_columns, show='headings')
for column in table_columns:
    table.heading(column, text=column)
table.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

input_frame = ttk.Frame(window)
input_frame.pack()

name_label = ttk.Label(input_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

value_label = ttk.Label(input_frame, text="Value:")
value_label.grid(row=1, column=0, padx=5, pady=5)
value_entry = ttk.Entry(input_frame)
value_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = ttk.Button(input_frame, text="Add Data", command=add_data)
add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

generate_button = ttk.Button(window, text="Generate Chart", command=generate_chart)
generate_button.pack(pady=10)

toggle_button = ttk.Button(window, text="Toggle Theme", command=toggle_theme)
toggle_button.pack(pady=10)

window.mainloop()
