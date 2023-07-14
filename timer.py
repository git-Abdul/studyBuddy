import customtkinter as ctk
import customtkinter
from plyer import notification
import threading

def start_timer():
    try:
        minutes = int(entry.get())
        seconds = minutes * 60

        timer_thread = threading.Thread(target=timer_countdown, args=(seconds,))
        timer_thread.start()

    except ValueError:
        notification.notify(
            title="Invalid Input",
            message="Please enter a valid number of minutes.",
            timeout=5  # Display notification for 5 seconds
        )

# Define the function to handle timer countdown and show notification
def timer_countdown(seconds):
    def show_notification():
        notification.notify(
            title="Study Timer",
            message="Timer has ended!",
            timeout=10,
            app_icon='icon.ico',
        )

    def update_stopwatch(remaining_seconds):
        minutes, secs = divmod(remaining_seconds, 60)
        stopwatch_label.configure(text=f"{minutes:02d}:{secs:02d}")
        if remaining_seconds > 0:
            stopwatch_label.after(1000, update_stopwatch, remaining_seconds - 1)
        else:
            show_notification()

    update_stopwatch(seconds)

# Create the GUI window
window = ctk.CTk()
window.title("Study Buddy • Timer")
window.iconbitmap('icon.ico')
window.resizable(False, False)
window.attributes("-topmost", True)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

entry = ctk.CTkEntry(window)
entry.grid(row=0, column=0, padx=10, pady=10)

start_button = ctk.CTkButton(window, text="Start", command=start_timer)
start_button.grid(row=1, column=0, padx=10, pady=10)

stopwatch_label = ctk.CTkLabel(window, font=ctk.CTkFont(size=40), text="00:00")
stopwatch_label.grid(row=2, column=0, padx=10, pady=10)

# Run the GUI main loop
window.mainloop()
