# home.py
import sys
import subprocess
import customtkinter
import os

def main():
    # Grab username from command line arguments; default to "User" if none given
    username = sys.argv[1] if len(sys.argv) > 1 else "User"

    # Create the main window, remove OS title bar
    home = customtkinter.CTk()
    home.overrideredirect(True)  # Removes native title bar and controls
    customtkinter.set_appearance_mode("System")

    # Fill entire screen
    screen_width = home.winfo_screenwidth()
    screen_height = home.winfo_screenheight()
    home.geometry(f"{screen_width}x{screen_height}+0+0")

    # Sidebar + partition total width
    sidebar_total = 480 + 2

    # Track maximize state and normal geometry
    is_maximized = True
    normal_geometry = None

    def set_full_screen():
        home.geometry(f"{screen_width}x{screen_height}+0+0")

    def minimize_window():
        home.iconify()

    def toggle_maximize():
        nonlocal is_maximized, normal_geometry
        if is_maximized:
            if normal_geometry:
                home.geometry(normal_geometry)
            else:
                home.geometry("1280x720+100+100")
            is_maximized = False
        else:
            normal_geometry = home.geometry()
            set_full_screen()
            is_maximized = True

    def close_window():
        home.destroy()

    # Start in full screen
    set_full_screen()
    home.update_idletasks()
    normal_geometry = home.geometry()

    # ---------------------------
    # Command Bar Function
    # ---------------------------
    def show_command_bar():
        cmd_bar = customtkinter.CTkToplevel(home)
        cmd_bar.overrideredirect(True)  # No native title bar
        # We set a black background. The corners won't be truly transparent on most systems.
        cmd_bar.configure(bg="#000000")  

        # Dimensions for the command bar
        width, height = 400, 300
        available_width = screen_width - sidebar_total
        x = sidebar_total + int((available_width - width) / 2)
        y = int((screen_height - height) / 2)
        cmd_bar.geometry(f"{width}x{height}+{x}+{y}")

        # Ensure the command bar grabs focus and can close on focus out or ESC
        cmd_bar.transient(home)
        cmd_bar.lift()
        cmd_bar.focus_force()

        # Close command bar on focus out (click outside)
        def on_focus_out(event):
            if not cmd_bar.winfo_containing(event.x_root, event.y_root):
                cmd_bar.destroy()

        # Bind events
        cmd_bar.bind("<FocusOut>", on_focus_out)
        cmd_bar.bind("<Escape>", lambda e: cmd_bar.destroy())

        # ---------------------------
        # Outer Frame with rounded corners & white border
        # ---------------------------
        # Note: The Toplevel won't literally have rounded corners on all platforms,
        # but this frame will appear rounded inside the window.
        outer_frame = customtkinter.CTkFrame(
            cmd_bar,
            corner_radius=20,           # Rounded corners
            border_width=2,            # 2-pixel border
            border_color="white",
            fg_color="#111111"         # dark background
        )
        outer_frame.pack(expand=True, fill="both")

        # ---------------------------
        # Inner Frame for the content
        # ---------------------------
        cmd_frame = customtkinter.CTkFrame(
            outer_frame,
            fg_color="#111111",
            corner_radius=20  # also set corner_radius here if you like
        )
        cmd_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Calculator button
        calc_button = customtkinter.CTkButton(
            cmd_frame,
            text="Calculator",
            fg_color="#333333",
            hover_color="#555555",
            text_color="white",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            command=lambda: subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "calculator.py")])
        )
        calc_button.pack(pady=10, fill="x")

        # Another task button (placeholder)
        sample_task_btn = customtkinter.CTkButton(
            cmd_frame,
            text="Another Task",
            fg_color="#333333",
            hover_color="#555555",
            text_color="white",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            command=lambda: None
        )
        sample_task_btn.pack(pady=10, fill="x")

        # Removed the close button from the command bar tasks
        # The user can close by ESC or clicking anywhere else

    # ---------------------------
    # Custom Top Bar (Arc-Inspired)
    # ---------------------------
    top_bar = customtkinter.CTkFrame(home, fg_color="#111111", height=40, corner_radius=0)
    top_bar.pack(side="top", fill="x")

    # Username button on left side of top bar
    username_btn = customtkinter.CTkButton(
        top_bar,
        text=username,
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        corner_radius=0,
        command=lambda: None
    )
    username_btn.pack(side="left", padx=10, pady=5)

    # Window control buttons on right side of top bar
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
        command=toggle_maximize
    )
    maximize_btn.pack(side="left", padx=2)

    close_btn = customtkinter.CTkButton(
        window_control_frame,
        text="X",
        width=30, height=30,
        corner_radius=5,
        fg_color="#111111",
        hover_color="#BB2222",
        text_color="white",
        command=close_window
    )
    close_btn.pack(side="left", padx=2)

    # ---------------------------
    # Main Content Area (Grey BG)
    # ---------------------------
    main_frame = customtkinter.CTkFrame(home, fg_color="#333333")
    main_frame.pack(fill="both", expand=True)

    # Left Sidebar
    sidebar_frame = customtkinter.CTkFrame(main_frame, width=480, fg_color="#111111")
    sidebar_frame.pack(side="left", fill="y")

    # Vertical partition
    partition = customtkinter.CTkFrame(main_frame, width=2, fg_color="#444444")
    partition.pack(side="left", fill="y")

    # "+ New Task" button in the sidebar triggers the command bar
    new_task_btn = customtkinter.CTkButton(
        sidebar_frame,
        text="+  New Task",
        fg_color="#111111",
        hover_color="#222222",
        text_color="white",
        corner_radius=0,
        command=show_command_bar
    )
    new_task_btn.pack(pady=(20, 0), padx=20, anchor="nw")

    # Main content area
    content_frame = customtkinter.CTkFrame(main_frame, fg_color="#333333")
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
