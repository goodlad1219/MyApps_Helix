import tkinter as tk

def add_task(event=None):
    task = task_entry.get()
    if task:
        task_listbox.insert(tk.END, f"• {task}")
        task_entry.delete(0, tk.END)

def delete_task(event):
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
    except IndexError:
        pass # Nothing selected

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

# --- Main App Window ---
app = tk.Tk()
app.title("Floating To-Do")
app.geometry("250x300")
app.configure(bg="#2d2d2d")

# Make it float on top and remove standard window borders
app.attributes("-topmost", True)
app.overrideredirect(True) 

# --- Dragging functionality ---
# Since we removed the title bar, we need a way to drag the window
drag_frame = tk.Frame(app, bg="#1e1e1e", height=20, cursor="fleur")
drag_frame.pack(fill=tk.X)
drag_frame.bind("<ButtonPress-1>", start_move)
drag_frame.bind("<ButtonRelease-1>", stop_move)
drag_frame.bind("<B1-Motion>", do_move)

# Close button inside the drag frame
close_btn = tk.Button(drag_frame, text="X", bg="#ff5f56", fg="white", bd=0, 
                      command=app.destroy, font=("Arial", 8, "bold"))
close_btn.pack(side=tk.RIGHT, padx=5)

# --- UI Elements ---
# Task List
task_listbox = tk.Listbox(app, bg="#2d2d2d", fg="white", bd=0, highlightthickness=0, 
                          font=("Arial", 12), selectbackground="#555555")
task_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
task_listbox.bind("<Double-Button-1>", delete_task) # Double click to remove

# Input Field
task_entry = tk.Entry(app, bg="#3d3d3d", fg="white", bd=0, highlightthickness=1, 
                      font=("Arial", 12), insertbackground="white")
task_entry.pack(pady=10, padx=10, fill=tk.X)
task_entry.bind("<Return>", add_task) # Press Enter to add

# Run the app
app.mainloop()