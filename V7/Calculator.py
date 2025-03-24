# Calculator.py
import customtkinter

class MacArcCalculatorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # ---------------------------
        # General Window Setup
        # ---------------------------
        self.title("Arc-Themed Calculator")
        self.geometry("350x550")  # Adjust as desired
        customtkinter.set_appearance_mode("System")  # or "Light" / "Dark"

        # Expression string to store what's typed
        self.expression = ""

        # Mapping for special symbols to Python operators
        self.operator_map = {
            "×": "*",
            "÷": "/"
        }

        # ---------------------------
        # Helper Functions
        # ---------------------------
        def on_button_click(char):
            """Handle button clicks for digits and operators."""
            if char == "=":
                calculate()
            elif char == "±":
                # Toggle sign of current expression or last number
                self.toggle_sign()
            else:
                # Map × and ÷ to * and /
                if char in self.operator_map:
                    self.expression += self.operator_map[char]
                else:
                    self.expression += str(char)
                self.display_var.set(self.expression)

        def calculate():
            """Evaluate the expression safely and display the result."""
            try:
                result = str(eval(self.expression))
                self.display_var.set(result)
                self.expression = result
            except:
                self.display_var.set("Error")
                self.expression = ""

        def clear():
            """Reset the display and expression."""
            self.expression = ""
            self.display_var.set("")

        # ---------------------------
        # Top Bar (Arc-Inspired) WITHOUT window-control icons
        # ---------------------------
        top_bar = customtkinter.CTkFrame(self, fg_color="#111111", height=40, corner_radius=0)
        top_bar.pack(side="top", fill="x")
        # (Optional) Add a title label
        # brand_label = customtkinter.CTkLabel(top_bar, text="Calculator", text_color="white")
        # brand_label.pack(side="left", padx=10, pady=5)

        # ---------------------------
        # Main Frame (Arc + Mac Style)
        # ---------------------------
        main_frame = customtkinter.CTkFrame(self, fg_color="#111111")
        main_frame.pack(fill="both", expand=True)

        # Display area
        self.display_var = customtkinter.StringVar()
        display_label = customtkinter.CTkLabel(
            main_frame,
            textvariable=self.display_var,
            font=customtkinter.CTkFont(size=32, weight="bold"),
            height=80,
            anchor="e",
            text_color="white",
            fg_color="#333333"  # darker gray for the display
        )
        display_label.pack(fill="x", pady=(10, 0), padx=10)

        # Grid frame for calculator buttons
        grid_frame = customtkinter.CTkFrame(main_frame, fg_color="#111111")
        grid_frame.pack(expand=True, fill="both", padx=10, pady=10)

        #I love macos ui and ux. Windows sucks in these areas.

        # Mac-style layout:
        # Row 1: [AC, ±, %, ÷]
        # Row 2: [7, 8, 9, ×]
        # Row 3: [4, 5, 6, –]
        # Row 4: [1, 2, 3, +]
        # Row 5: [0, ., =]  (0 spans two columns)
        # We'll store them as (text, bg_color, hover_color, col_span)
        buttons_config = [
            [("AC", "#A5A5A5", "#B5B5B5", 1),
             ("±",  "#A5A5A5", "#B5B5B5", 1),
             ("%",  "#A5A5A5", "#B5B5B5", 1),
             ("÷",  "#FF9500", "#FFB347", 1)],

            [("7", "#333333", "#444444", 1),
             ("8", "#333333", "#444444", 1),
             ("9", "#333333", "#444444", 1),
             ("×", "#FF9500", "#FFB347", 1)],

            [("4", "#333333", "#444444", 1),
             ("5", "#333333", "#444444", 1),
             ("6", "#333333", "#444444", 1),
             ("-", "#FF9500", "#FFB347", 1)],

            [("1", "#333333", "#444444", 1),
             ("2", "#333333", "#444444", 1),
             ("3", "#333333", "#444444", 1),
             ("+", "#FF9500", "#FFB347", 1)],

            [("0", "#333333", "#444444", 2),  # col_span=2
             (".", "#333333", "#444444", 1),
             ("=", "#FF9500", "#FFB347", 1)],
        ]

        # Build the grid
        row_count = 0
        for row_vals in buttons_config:
            col_count = 0
            for (text, fg_col, hover_col, col_span) in row_vals:
                button = customtkinter.CTkButton(
                    grid_frame,
                    text=text,
                    width=60,
                    height=60,
                    corner_radius=0,
                    fg_color=fg_col,
                    hover_color=hover_col,
                    text_color="white",
                    font=customtkinter.CTkFont(size=18, weight="bold"),
                    command=lambda char=text: self.handle_button_click(char, on_button_click, clear)
                )
                button.grid(row=row_count, column=col_count, columnspan=col_span, padx=5, pady=5, sticky="nsew")
                col_count += col_span
            row_count += 1

        # Configure grid weights for even spacing
        for i in range(4):  # 4 columns
            grid_frame.columnconfigure(i, weight=1)
        for i in range(5):  # 5 rows
            grid_frame.rowconfigure(i, weight=1)

    def handle_button_click(self, char, on_button_click, clear):
        """Special handling for AC vs others."""
        if char == "AC":
            clear()
        else:
            on_button_click(char)

    def toggle_sign(self):
        """Toggle sign of the current expression or last number."""
        # If expression is empty, do nothing
        if not self.expression:
            return
        try:
            # Convert expression to float, multiply by -1
            val = float(self.expression)
            val *= -1
            self.expression = str(val)
            self.display_var.set(self.expression)
        except ValueError:
            # If expression isn't purely numeric, 
            # you might want more advanced logic to handle partial sign toggles.
            pass

def main():
    app = MacArcCalculatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
