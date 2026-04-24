import tkinter as tk

# --- Defined Aesthetic Variables ---
BG_COLOR = "#000000"       # Total Black
GREEN_THEME = "#00ff00"   # Matrix Green
FONT_STYLE = ("Consolas", 12) # Classic coding font (or Courier New)
ALPHA_LEVEL = 0.8          # 80% opaque (20% transparent)

def add_task(event=None):
    task = task_entry.get()
    if task:
        # Styled prefix for tasks [++]
        task_listbox.insert(tk.END, f"[++] {task}")
        task_entry.delete(0, tk.END)

def delete_task(event):
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
    except IndexError:
        pass # Nothing selected or empty list double-click

# --- Window Dragging functionality ---
def start_move(event):
    app.x = event.x
    app.y = event.y

def stop_move(event):
    app.x = None
    app.y = None

def do_move(event):
    deltax = event.x - app.x
    deltay = event.y - app.y
    x = app.winfo_x() + deltax
    y = app.winfo_y() + deltay
    app.geometry(f"+{x}+{y}")

# --- Main App Window Setup ---
app = tk.Tk()
app.title("Neural_Link v1.0") # Factual, Cyberpunk title
app.geometry("260x320")
app.configure(bg=BG_COLOR)

# --- Aesthetic Attributes ---
# 1. Keep always on top
app.attributes("-topmost", True)
# 2. Remove standard OS window borders
app.overrideredirect(True) 
# 3. Set transparency level (0.0 full transparent - 1.0 full opaque)
app.attributes("-alpha", ALPHA_LEVEL)

# --- Cyberpunk Drag Frame (Since OS borders are gone) ---
drag_frame = tk.Frame(app, bg="#0a0a0a", height=25, cursor="fleur")
drag_frame.pack(fill=tk.X)
drag_frame.bind("<ButtonPress-1>", start_move)
drag_frame.bind("<ButtonRelease-1>", stop_move)
drag_frame.bind("<B1-Motion>", do_move)

# Faux-terminal text in drag frame
title_lbl = tk.Label(drag_frame, text="// SYSTEM.TRACKER", bg="#0a0a0a", fg=GREEN_THEME,
                     font=("Consolas", 10, "bold"))
title_lbl.pack(side=tk.LEFT, padx=5)

# Styled close button
close_btn = tk.Button(drag_frame, text="[X]", bg="#0a0a0a", fg="#ff0000", bd=0, 
                      command=app.destroy, font=("Arial", 10, "bold"), activebackground="#1a1a1a")
close_btn.pack(side=tk.RIGHT, padx=5)

# Separator line beneath the drag frame
sep_line = tk.Frame(app, bg=GREEN_THEME, height=2)
sep_line.pack(fill=tk.X)

# --- Task List UI Element ---
task_listbox = tk.Listbox(app, 
                          bg=BG_COLOR,             # Match window bg
                          fg=GREEN_THEME,          # Green text
                          font=FONT_STYLE,
                          bd=0,                   # No border
                          highlightthickness=0,    # No focus border
                          selectbackground="#222222", # Slight highlight for selection
                          activestyle="none")      # No underlined item
task_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Double click to remove
task_listbox.bind("<Double-Button-1>", delete_task) 

# --- Input Field UI Element ---
task_entry = tk.Entry(app, 
                      bg="#0a0a0a",           # Slightly lighter dark bg
                      fg=GREEN_THEME,          # Green input text
                      font=FONT_STYLE,
                      insertbackground=GREEN_THEME, # Green cursor
                      bd=0,                   # No native border
                      highlightthickness=1,    # We will use focus border
                      highlightbackground="#1a1a1a", # Default focus color
                      highlightcolor=GREEN_THEME)  # Highlighted focus color
task_entry.pack(pady=15, padx=10, fill=tk.X)

# We bind 'FocusIn' to clear default text if we add any, 
# and 'Return' (Enter) to add the task
task_entry.bind("<Return>", add_task) 

# Initial filler content for effect
task_entry.insert(0, "> input_task_")

def clear_entry(event):
    if task_entry.get() == "> input_task_":
        task_entry.delete(0, tk.END)

task_entry.bind("<FocusIn>", clear_entry)

# --- Bottom Status Label for aesthetic ---
status_lbl = tk.Label(app, text="STATUS: CONNECTED", bg=BG_COLOR, fg=GREEN_THEME,
                      font=("Consolas", 8), anchor="w")
status_lbl.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=2)

# --- Run the widget ---
app.mainloop()