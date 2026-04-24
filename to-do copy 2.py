import tkinter as tk
import os

# --- Defined Aesthetic Variables ---
BG_COLOR = "#000000"
GREEN_THEME = "#00ff00"
FONT_STYLE = ("Consolas", 12)
ALPHA_LEVEL = 0.8
DATA_FILE = "neural_log.dat" # The file where your tasks will live

class NeuralWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural_Link v3.0")
        
        # --- Window States & Sizes ---
        self.full_w, self.full_h = 280, 360 # Made slightly larger to accommodate new buttons
        self.mini_w, self.mini_h = 60, 60
        self.is_minimized = False
        
        # Apply initial settings
        self.root.geometry(f"{self.full_w}x{self.full_h}")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", ALPHA_LEVEL)
        
        # ==========================================
        # 1. BUILD THE FULL TERMINAL UI
        # ==========================================
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top Drag Bar
        self.drag_frame = tk.Frame(self.main_frame, bg="#0a0a0a", height=25, cursor="fleur")
        self.drag_frame.pack(fill=tk.X)
        
        self.title_lbl = tk.Label(self.drag_frame, text="// SYSTEM.TRACKER", bg="#0a0a0a", fg=GREEN_THEME, font=("Consolas", 10, "bold"), cursor="fleur")
        self.title_lbl.pack(side=tk.LEFT, padx=5)
        
        # Close Window Button (True Exit)
        self.close_btn = tk.Button(self.drag_frame, text="[X]", bg="#0a0a0a", fg="#ff0000", bd=0, command=self.root.destroy, font=("Arial", 10, "bold"), activebackground="#1a1a1a")
        self.close_btn.pack(side=tk.RIGHT, padx=5)

        # Collapse Button (Fold to Circle)
        self.collapse_btn = tk.Button(self.drag_frame, text="[-]", bg="#0a0a0a", fg=GREEN_THEME, bd=0, command=self.collapse, font=("Arial", 10, "bold"), activebackground="#1a1a1a")
        self.collapse_btn.pack(side=tk.RIGHT, padx=5)
        
        tk.Frame(self.main_frame, bg=GREEN_THEME, height=2).pack(fill=tk.X)
        
        # Task List (Naturally scrollable with mouse wheel)
        self.task_listbox = tk.Listbox(self.main_frame, bg=BG_COLOR, fg=GREEN_THEME, font=FONT_STYLE, bd=0, highlightthickness=0, selectbackground="#222222", activestyle="none")
        self.task_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.task_listbox.bind("<Double-Button-1>", self.delete_task)
        
        # Input Field
        self.task_entry = tk.Entry(self.main_frame, bg="#0a0a0a", fg=GREEN_THEME, font=FONT_STYLE, insertbackground=GREEN_THEME, bd=0, highlightthickness=1, highlightbackground="#1a1a1a", highlightcolor=GREEN_THEME)
        self.task_entry.pack(pady=10, padx=10, fill=tk.X)
        self.task_entry.bind("<Return>", self.add_task)
        self.task_entry.insert(0, "> input_task_")
        self.task_entry.bind("<FocusIn>", self.clear_entry)
        
        # Bottom Status & Action Bar
        self.bottom_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=5, side=tk.BOTTOM)

        # Clear All Button
        self.clear_btn = tk.Button(self.bottom_frame, text="[PURGE]", bg=BG_COLOR, fg="#ffaa00", bd=0, font=("Consolas", 10, "bold"), activebackground="#222222", command=self.clear_all_tasks)
        self.clear_btn.pack(side=tk.LEFT)

        # Status Label
        self.status_lbl = tk.Label(self.bottom_frame, text="STATUS: ONLINE", bg=BG_COLOR, fg=GREEN_THEME, font=("Consolas", 8), cursor="fleur")
        self.status_lbl.pack(side=tk.RIGHT)

        # ==========================================
        # 2. BUILD THE COLLAPSED ICON
        # ==========================================
        self.icon_frame = tk.Frame(self.root, bg=BG_COLOR, cursor="fleur")
        self.icon_canvas = tk.Canvas(self.icon_frame, width=60, height=60, bg=BG_COLOR, bd=0, highlightthickness=0)
        self.icon_canvas.pack()
        
        self.icon_canvas.create_oval(10, 10, 50, 50, outline=GREEN_THEME, width=2)
        self.icon_canvas.create_oval(20, 20, 40, 40, fill=GREEN_THEME)
        self.icon_canvas.bind("<Double-Button-1>", lambda e: self.expand())
        
        # ==========================================
        # 3. INITIALIZE LOGIC & DRAGGING
        # ==========================================
        self.setup_dragging()
        self.load_tasks() # Load saved data on startup
        
    # --- Task & Data Logic ---
    def add_task(self, event=None):
        task = self.task_entry.get().strip()
        if task and task != "> input_task_":
            self.task_listbox.insert(tk.END, f"[++] {task}")
            self.task_entry.delete(0, tk.END)
            self.save_tasks()

    def delete_task(self, event):
        try:
            selected = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected)
            self.save_tasks()
        except IndexError:
            pass

    def clear_all_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.save_tasks()

    def clear_entry(self, event):
        if self.task_entry.get() == "> input_task_":
            self.task_entry.delete(0, tk.END)

    # --- File System Persistence ---
    def save_tasks(self):
        with open(DATA_FILE, "w") as file:
            tasks = self.task_listbox.get(0, tk.END)
            for task in tasks:
                file.write(task + "\n")

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                tasks = file.readlines()
                for task in tasks:
                    if task.strip(): # Ignore empty lines
                        self.task_listbox.insert(tk.END, task.strip())

    # --- Animation & State Engine ---
    def collapse(self):
        if not self.is_minimized:
            self.is_minimized = True
            self.main_frame.pack_forget() 
            self.animate_window(self.full_w, self.full_h, self.mini_w, self.mini_h, self.show_icon)

    def expand(self):
        if self.is_minimized:
            self.is_minimized = False
            self.icon_frame.pack_forget() 
            self.animate_window(self.mini_w, self.mini_h, self.full_w, self.full_h, self.show_main)

    def show_icon(self):
        self.icon_frame.pack(fill=tk.BOTH, expand=True)
        
    def show_main(self):
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def animate_window(self, start_w, start_h, end_w, end_h, callback, step=0):
        total_steps = 15
        if step <= total_steps:
            current_w = int(start_w + (end_w - start_w) * (step / total_steps))
            current_h = int(start_h + (end_h - start_h) * (step / total_steps))
            self.root.geometry(f"{current_w}x{current_h}")
            self.root.after(10, self.animate_window, start_w, start_h, end_w, end_h, callback, step + 1)
        else:
            callback()

    # --- Dragging Physics ---
    def setup_dragging(self):
        for element in (self.drag_frame, self.title_lbl, self.icon_canvas, self.status_lbl):
            element.bind("<ButtonPress-1>", self.start_move)
            element.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_win_x = self.root.winfo_x()
        self.start_win_y = self.root.winfo_y()

    def do_move(self, event):
        deltax = event.x_root - self.start_x
        deltay = event.y_root - self.start_y
        x = self.start_win_x + deltax
        y = self.start_win_y + deltay
        self.root.geometry(f"+{x}+{y}")

# --- Application Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = NeuralWidget(root)
    root.mainloop()