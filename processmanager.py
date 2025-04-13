#!/bin/python3
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

REFRESH_INTERVAL = 1000

def refresh_processes():
    # Run 'ps aux' and split the output into lines
    result = subprocess.run(['ps','aux'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    
    # First line is the header
    headers = lines[0].split()
    
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data
    for line in lines[1:]:
        # Split the line into fields based on whitespace
        parts = line.split(None, len(headers) - 1)
        tree.insert('', tk.END, values=parts)

    # Schedule next refresh
    root.after(REFRESH_INTERVAL, refresh_processes)
def killprocess():
        to_kill = entry.get()
        subprocess.run(["kill", to_kill])
        messagebox.showinfo("Process Killed", f"PID: {to_kill} has been stopped!")
def log():
	logdata = subprocess.run("ps", capture_output=True, text=True)
	try:
		f = open("log.txt","a")
		current = str(datetime.datetime.now())
		f.write(current + ":\n")
		f.write(logdata.stdout.strip() + "\n\n")
		print("saved successfully!")
	except:
		print("save fail")
		pass
	f.close()
# Setup window
root = tk.Tk()
root.title("Process Viewer (ps) - Task manager")

# Create Treeview
tree = ttk.Treeview(root, columns=[], show='headings', height=25)
tree.pack(fill=tk.BOTH, expand=True)

# Run ps once to get headers and set columns
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
lines = result.stdout.strip().split('\n')
headers = lines[0].split()

# Set up columns
tree['columns'] = headers
for col in headers:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='w')
    
#input field
input_frame = tk.Frame(root)
input_frame.pack(pady=5)
entry = tk.Entry(input_frame, width=30)
entry.pack(side=tk.LEFT, padx=5)

#Entry submit btn
submit_btn = tk.Button(input_frame, text="END TASK", command =killprocess)
submit_btn.pack(side=tk.LEFT)

#Log save button
log_frame = tk.Frame(root)
log_frame.pack(pady =5)
log_btn = tk.Button(log_frame, text="save simplified log",command =log)
log_btn.pack(side=tk.LEFT, padx=5)

# Start auto-refresh
refresh_processes()

# Run GUI
root.mainloop()
