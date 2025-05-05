import datetime
from time import gmtime
import sqlite3
import subprocess
import os

def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window.winfo_reqwidth()) // 2
    y = (screen_height - window.winfo_reqheight()) // 2
    window.geometry(f"+{x}+{y}")

def logSignInSignOutTime(SignIn: bool, UserName: str):
    print('logSignInSignOutTime')
    currentTime = datetime.datetime.now()
    
    if SignIn == False:
        loginTime = ''
        logoutTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        mySql = f"UPDATE users set signOutTime = '{logoutTime}' where username='{UserName}'"
        print(logoutTime)
    else:
        logoutTime = ''
        loginTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        mySql = f"UPDATE users set signInTime = '{loginTime}' where username='{UserName}'"
        print(loginTime)
        
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute(f'{mySql}')

    # Commit the changes
    connection.commit()
        
    # Close the connection
    connection.close()
    
def setUserName(newUserName: str, UserName: str):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    mySql = f"UPDATE users set username = '{newUserName}' where username='{UserName}'"
    cursor.execute(f'{mySql}')

    # Commit the changes
    connection.commit()
        
    # Close the connection
    connection.close()
    users_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "users")
    old_path = os.path.join(users_dir, UserName)
    new_path = os.path.join(users_dir, newUserName)
    os.rename(old_path, new_path)
    print(f"Folder '{old_path}' successfully renamed to '{new_path}'.")
    
def setUserColor(ColorCode: str, UserName: str):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    mySql = f"UPDATE users set usercolor = '{ColorCode}' where username='{UserName}'"
    cursor.execute(f'{mySql}')

    # Commit the changes
    connection.commit()
        
    # Close the connection
    connection.close()
    
def setUserTheme(ThemeCode: str, UserName: str):
    print(ThemeCode)
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    mySql = f"UPDATE users set usertheme = '{ThemeCode}' where username='{UserName}'"
    cursor.execute(f'{mySql}')

    # Commit the changes
    connection.commit()
        
    # Close the connection
    connection.close()
    
def reopen_signInPage(window):
    window.destroy()
    subprocess.run(["python", "main.py"])
    
def reopen_window(window, signed_in_user, logout_time, user_color, user_theme):
    # Close the current window and reopen it with the same parameters
    window.destroy()
    subprocess.run(["python", "home.py", signed_in_user, logout_time, user_color, user_theme])