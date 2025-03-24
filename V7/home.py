# home.py
import sys
import customtkinter

# Track full screen toggle state globally
full_screen = False

def main():
    # Grab username from command line arguments; default to "User" if none given
    username = sys.argv[1] if len(sys.argv) > 1 else "User"

    # Create the main window
    home = customtkinter.CTk()
    home.title("Study Buddy • Home")
    home.geometry("1280x720")  # Adjust as desired

    # ------------------------------------------------
    # Functions for Window Control (min/max/fullscreen)
    # ------------------------------------------------
    def minimize_window():
        home.iconify()

    def maximize_window():
        if home.state() == "normal":
            home.state("zoomed")
        else:
            home.state("normal")

    def toggle_fullscreen():
        global full_screen
        full_screen = not full_screen
        home.attributes("-fullscreen", full_screen)

    # ---------------------------
    # Top Bar (integrated in the app)
    # ---------------------------
    # Using #111111 so it matches the sidebar
    top_bar = customtkinter.CTkFrame(home, fg_color="#111111", height=40, corner_radius=0)
    top_bar.pack(side="top", fill="x")

    # Left side: username button
    username_btn = customtkinter.CTkButton(
        top_bar,
        text=username,
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        corner_radius=0,
        command=lambda: None  # No function yet
    )
    username_btn.pack(side="left", padx=10, pady=5)

    # Right side: Window control buttons
    window_control_frame = customtkinter.CTkFrame(top_bar, fg_color="#111111", corner_radius=0)
    window_control_frame.pack(side="right", padx=5, pady=5)

    minimize_btn = customtkinter.CTkButton(
        window_control_frame,
        text="–",
        width=30, height=30,
        corner_radius=5,
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        command=minimize_window
    )
    minimize_btn.pack(side="left", padx=2)

    maximize_btn = customtkinter.CTkButton(
        window_control_frame,
        text="▢",
        width=30, height=30,
        corner_radius=5,
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        command=maximize_window
    )
    maximize_btn.pack(side="left", padx=2)

    fullscreen_btn = customtkinter.CTkButton(
        window_control_frame,
        text="⛶",
        width=30, height=30,
        corner_radius=5,
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        command=toggle_fullscreen
    )
    fullscreen_btn.pack(side="left", padx=2)

    # ---------------------------
    # Main Content Area (Black BG)
    # ---------------------------
    # Full-frame to hold sidebar + main area
    main_frame = customtkinter.CTkFrame(home, fg_color="black")
    main_frame.pack(fill="both", expand=True)

    # ---------------------------
    # Left Sidebar (width=480)
    # ---------------------------
    # Also #111111 to match top bar
    sidebar_frame = customtkinter.CTkFrame(main_frame, width=480, fg_color="#111111")
    sidebar_frame.pack(side="left", fill="y")

    # Visible vertical partition
    partition = customtkinter.CTkFrame(main_frame, width=2, fg_color="#444444")
    partition.pack(side="left", fill="y")

    # Only "New Task" remains in the sidebar, as a button with no function
    new_task_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="+  New Task",
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        corner_radius=0,
        command=lambda: None  # No function yet
    )
    new_task_btn.pack(pady=(20, 0), padx=20, anchor="nw")

    # ---------------------------
    # Main Content (right area)
    # ---------------------------
    content_frame = customtkinter.CTkFrame(main_frame, fg_color="black")
    content_frame.pack(side="left", fill="both", expand=True)

    welcome_label = customtkinter.CTkLabel(
        content_frame,
        text="Welcome to Study Buddy Home!",
        font=customtkinter.CTkFont(size=24, weight="bold"),
        text_color="white"
    )
    welcome_label.pack(pady=50)

    home.mainloop()

if __name__ == "__main__":
    main()
