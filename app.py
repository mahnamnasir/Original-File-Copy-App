import hashlib
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

def file_hash(filename):
    # This function calculates the hash of a file
    hash_obj = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def copy_original_files(source_directory, destination_directory):
    # This function finds and copies one original file for each duplicate in a directory
    file_hashes = {}

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_info = (file_size, file_hash(file_path))

            if file_info in file_hashes:
                original_file_path = file_hashes[file_info]
                destination_path = os.path.join(destination_directory, os.path.basename(original_file_path))
                if not os.path.exists(destination_path):
                    shutil.copy2(original_file_path, destination_path)
            else:
                file_hashes[file_info] = file_path

def browse_source_directory():
    source_dir = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_dir)

def browse_destination_directory():
    dest_dir = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, dest_dir)

def copy_files_from_source_to_destination():
    source_directory = source_entry.get()
    destination_directory = destination_entry.get()

    if not source_directory or not destination_directory:
        messagebox.showerror("Error", "Both source and destination directories must be specified.")
        return

    if not os.path.exists(source_directory):
        messagebox.showerror("Error", "Source directory does not exist.")
        return

    try:
        os.makedirs(destination_directory, exist_ok=True)
        copy_original_files(source_directory, destination_directory)
        messagebox.showinfo("Success", "Files copied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

app = tk.Tk()
app.title("Duplicate File Finder")
app.geometry("400x250")  # Adjust the dimensions as needed

source_label = tk.Label(app, text="Source Directory:")
source_label.pack(pady=5)
source_entry = tk.Entry(app)
source_entry.pack(pady=5)
source_browse_button = tk.Button(app, text="Browse", command=browse_source_directory)
source_browse_button.pack(pady=5)

destination_label = tk.Label(app, text="Destination Directory:")
destination_label.pack(pady=5)
destination_entry = tk.Entry(app)
destination_entry.pack(pady=5)
destination_browse_button = tk.Button(app, text="Browse", command=browse_destination_directory)
destination_browse_button.pack(pady=5)

copy_button = tk.Button(app, text="Copy Original Files", command=copy_files_from_source_to_destination)
copy_button.pack(pady=10)

app.mainloop()
