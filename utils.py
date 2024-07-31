import datetime
from time import gmtime
import sqlite3
import subprocess

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
    
def reopen_window(window, signed_in_user, logout_time, user_color, user_theme):
    # Close the current window and reopen it with the same parameters
    window.destroy()
    subprocess.run(["python", "home.py", signed_in_user, logout_time, user_color, user_theme])