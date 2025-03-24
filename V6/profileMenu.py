import customtkinter
from PIL import Image, ImageTk
import datetime
from plyer import notification
from time import gmtime
import sqlite3
from utils import setUserName
import sys, os, time, signal, psutil

username = sys.argv[1]
usercolor = sys.argv[2]
usertheme = sys.argv[4]

customtkinter.set_default_color_theme(usercolor)
customtkinter.set_appearance_mode(usertheme)

app = customtkinter.CTk()
app.title(f"Studybuddy • Profile")
app.geometry("420x420")
app.iconbitmap("icon.ico")
app.resizable(False, False)

def create_file(file_path, content=""):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"Error creating file '{file_path}': {e}")
        
def editPassword():
    dialog = customtkinter.CTkInputDialog(text="Type in your password:", title="Edit Password")
    newPassword = dialog.get_input()
    
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
           
    mySql = f"UPDATE users set password = '{newPassword}' where username='{username}'"
    cursor.execute(f'{mySql}')

    # Commit the changes
    connection.commit()
            
    # Close the connection
    connection.close()
        
    file_path = "ProfileChanges.txt"
    file_content = f"Password changed to {newPassword}"

    create_file(file_path, file_content)
        
    time.sleep(1.5)   
    app.destroy()

def editUserName():
    dialog = customtkinter.CTkInputDialog(text="Type in your username:", title="Edit Username")
    newUserName = dialog.get_input()
    count = int(0)
    
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT username FROM users")

    # Fetch all results
    rows = cursor.fetchall()

    for row in rows:
        if(row[0] == newUserName):
            count = count + 1
            
    if(count>=1):
        notification.notify(
            title="Username already exists.",
            message="Please enter a valid username.",
            timeout=5  # Display notification for 5 seconds
        )
        connection.close()
    else:              
        mySql = f"UPDATE users set username = '{newUserName}' where username='{username}'"
        cursor.execute(f'{mySql}')

        # Commit the changes
        connection.commit()
            
        # Close the connection
        connection.close()
        users_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
        old_path = os.path.join(users_dir, username)
        new_path = os.path.join(users_dir, newUserName)
        
        os.rename(old_path, new_path)
        print(f"Folder '{old_path}' successfully renamed to '{new_path}'.")
        
        file_path = "ProfileChanges.txt"
        file_content = f"Username changed from {username} to {newUserName}"

        create_file(file_path, file_content)
        
        time.sleep(1.5)
        
        app.destroy()
        

    
try:
    profile_image = Image.open("profile_pic.png")
    profile_image = profile_image.resize((50, 50))
    profile_photo = ImageTk.PhotoImage(profile_image)
    profile_label = customtkinter.CTkLabel(app, image=profile_photo, text="")
    profile_label.image = profile_photo
    profile_label.pack(pady=(20, 0))
except FileNotFoundError:
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "_images")
    if(usercolor == "blue"):
        profile_image = Image.open(os.path.join(image_path, "profilePlaceholder-Blue.png"))
    elif(usercolor == "dark-blue"):
        profile_image = Image.open(os.path.join(image_path, "profilePlaceholder-DBlue.png"))
    else:
        profile_image = Image.open(os.path.join(image_path, "profilePlaceholder-Green.png"))
    profile_image = profile_image.resize((120, 120))
    profile_photo = ImageTk.PhotoImage(profile_image)
    profile_label = customtkinter.CTkLabel(app, image=profile_photo, text="")
    profile_label.image = profile_photo
    profile_label.pack(pady=(20, 0))
    
ctkFont = customtkinter.CTkFont(
    family="Inter",
    size=20
)
    
usernameLabel = customtkinter.CTkLabel(app, text=username, font=ctkFont)
usernameLabel.pack(pady=20)

#Edit Username
frame = customtkinter.CTkFrame(app, width=300, height=50, border_width=1, border_color="#1f1f1f",)
frame.pack(pady=5)

text_label = customtkinter.CTkLabel(frame, text=f"Username: {username}", anchor="w") 
text_label.place(x=10, rely=0.5, anchor="w")  

button = customtkinter.CTkButton(frame, text="Edit", width=60, height=30, command=editUserName) 
button.place(relx=0.95, rely=0.5, anchor="e") 

#Edit Password
frame = customtkinter.CTkFrame(app, width=300, height=50, border_width=1, border_color="#1f1f1f",)
frame.pack(pady=5)

text_label = customtkinter.CTkLabel(frame, text=f"Edit Password", anchor="w") 
text_label.place(x=10, rely=0.5, anchor="w")  

button = customtkinter.CTkButton(frame, text="Edit", width=60, height=30, command=editPassword) 
button.place(relx=0.95, rely=0.5, anchor="e") 

frame = customtkinter.CTkFrame(app, width=300, height=50, border_width=1, border_color="#1f1f1f",)
frame.pack(pady=5)

text_label = customtkinter.CTkLabel(frame, text="StudyBuddy Version: ", anchor="w") 
text_label.place(x=10, rely=0.5, anchor="w")  

buttonVer = customtkinter.CTkButton(frame, text="6.0", width=60, height=30, text_color_disabled="white")
buttonVer.place(relx=0.95, rely=0.5, anchor="e") 

buttonVer.configure(state="disabled")

app.mainloop()