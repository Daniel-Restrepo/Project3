import tkinter as tk
import file_operations as fileops

from pathlib import Path
from tkinter import simpledialog, messagebox
from datetime import datetime

# --- Set_up paths ---
PROJECT_FOLDER = Path(__file__).parent
START_FOLDER = PROJECT_FOLDER / "test_files"
START_FOLDER.mkdir(exist_ok=True)

current_path = START_FOLDER

# --- GUI setup ---
window = tk.Tk()
window.title("CS 3502 File Manager")
window.geometry("950x780")

# Path label
path_label = tk.Label(window, text=f"Current Path: {current_path}")
path_label.pack(pady=10)

#file label
files_label = tk.Label(window, text="Files and Folders")
files_label.pack()

# File list
file_listbox = tk.Listbox(window, width=80, height=20)
file_listbox.pack(pady=10)

# Status label
status_label = tk.Label(window, text="Ready")
status_label.pack(pady=10)

#edit Label
editor_label = tk.Label(window, text="File Contents")
editor_label.pack()
#--- Function to load files ---
def load_files():
    file_listbox.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

    try:
        for item in fileops.list_items(current_path):
            if item.is_dir():
                file_listbox.insert(tk.END, f"[DIR] {item.name}")
            else:
                file_listbox.insert(tk.END, item.name)

        status_label.config(text="Files loaded successfully")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

#Text area
content_text = tk.Text(window, width=80, height=10)
content_text.pack(pady=10)

#------------------ Functions -----------------------
def open_selected_file():
    selected = file_listbox.curselection()

    if not selected:
        status_label.config(text="Please select a file first")
        return

    file_name = file_listbox.get(selected[0])

    if file_name.startswith("[DIR]"):
        status_label.config(text="That is a folder, not a file")
        return

    file_path = current_path / file_name

    try:
        content = fileops.read_file(file_path)

        content_text.delete("1.0", tk.END)
        content_text.insert(tk.END, content)

        status_label.config(text=f"Opened file: {file_name}")

    except PermissionError:
        status_label.config(text="Permission denied: cannot read this file")
    except Exception as e:
        status_label.config(text=f"Error opening file: {str(e)}")


def save_selected_file():
    selected = file_listbox.curselection()

    if not selected:
        status_label.config(text="Please select a file first")
        return

    file_name = file_listbox.get(selected[0])

    if file_name.startswith("[DIR]"):
        status_label.config(text="That is a folder, not a file")
        return

    file_path = current_path / file_name

    try:
        new_content = content_text.get("1.0", tk.END)

        fileops.save_file(file_path, new_content)

        status_label.config(text=f"Saved changes to: {file_name}")

    except PermissionError:
        status_label.config(text="Permission denied: cannot update this file")
    except Exception as e:
        status_label.config(text=f"Error saving file: {str(e)}")


def create_file():
    file_name = simpledialog.askstring("Create File", "Enter file name:")

    if not file_name:
        status_label.config(text="Create file cancelled")
        return

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    file_path = current_path / file_name

    try:
        fileops.create_file(file_path)

        load_files()
        status_label.config(text=f"Created file: {file_name}")

    except FileExistsError:
        status_label.config(text="File already exists")
    except PermissionError:
        status_label.config(text="Permission denied: cannot create file here")
    except Exception as e:
        status_label.config(text=f"Error creating file: {str(e)}")


def delete_selected_item():
    selected = file_listbox.curselection()

    if not selected:
        status_label.config(text="Please select a file or folder first")
        return

    item_name = file_listbox.get(selected[0])

    if item_name.startswith("[DIR] "):
        item_name = item_name.replace("[DIR] ", "", 1)

    item_path = current_path / item_name

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{item_name}'?"
    )

    if not confirm:
        status_label.config(text="Delete cancelled")
        return

    try:
        fileops.delete_item(item_path)

        load_files()
        content_text.delete("1.0", tk.END)
        status_label.config(text=f"Deleted: {item_name}")

    except PermissionError:
        status_label.config(text="Permission denied: cannot delete this item")
    except OSError as e:
        status_label.config(text=f"Error deleting item: {str(e)}")


def rename_selected_item():
    selected = file_listbox.curselection()

    if not selected:
        status_label.config(text="Please select a file or folder first")
        return

    old_name = file_listbox.get(selected[0])

    if old_name.startswith("[DIR] "):
        old_name = old_name.replace("[DIR] ", "", 1)

    old_path = current_path / old_name

    new_name = simpledialog.askstring("Rename", "Enter new name:")

    if not new_name:
        status_label.config(text="Rename cancelled")
        return

    new_path = current_path / new_name

    if new_path.exists():
        confirm = messagebox.askyesno(
            "Overwrite?",
            f"'{new_name}' already exists. Overwrite?"
        )

        if not confirm:
            status_label.config(text="Rename cancelled")
            return

    try:
        fileops.rename_item(old_path, new_path)

        load_files()
        status_label.config(text=f"Renamed '{old_name}' to '{new_name}'")

    except FileExistsError:
        status_label.config(text="A file or folder with that name already exists")
    except PermissionError:
        status_label.config(text="Permission denied: cannot rename this item")
    except Exception as e:
        status_label.config(text=f"Error renaming item: {str(e)}")


def create_folder():
    folder_name = simpledialog.askstring("Create Folder", "Enter folder name:")

    if not folder_name:
        status_label.config(text="Create folder cancelled")
        return

    folder_path = current_path / folder_name

    try:
        fileops.create_folder(folder_path)
        load_files()
        status_label.config(text=f"Created folder: {folder_name}")

    except FileExistsError:
        status_label.config(text="Folder already exists")
    except PermissionError:
        status_label.config(text="Permission denied: cannot create folder here")
    except Exception as e:
        status_label.config(text=f"Error creating folder: {str(e)}")


def open_selected_item(event=None):
    global current_path

    selected = file_listbox.curselection()

    if not selected:
        status_label.config(text="Please select a file or folder first")
        return

    item_name = file_listbox.get(selected[0])

    if item_name.startswith("[DIR] "):
        folder_name = item_name.replace("[DIR] ", "", 1)
        folder_path = current_path / folder_name

        try:
            current_path = folder_path
            path_label.config(text=f"Current Path: {current_path}")
            content_text.delete("1.0", tk.END)
            load_files()
            status_label.config(text=f"Opened folder: {folder_name}")

        except PermissionError:
            status_label.config(text="Permission denied: cannot open this folder")
        except Exception as e:
            status_label.config(text=f"Error opening folder: {str(e)}")
    else:
        open_selected_file()


def go_up_one_folder():
    global current_path

    if current_path == START_FOLDER:
        status_label.config(text="Already at the starting folder")
        return

    current_path = current_path.parent
    path_label.config(text=f"Current Path: {current_path}")
    content_text.delete("1.0", tk.END)
    load_files()
    status_label.config(text="Moved up one folder")


def show_properties():
    selected = file_listbox.curselection()

    if not selected:
        status_label.config(text="Please select a file or folder first")
        return

    item_name = file_listbox.get(selected[0])

    if item_name.startswith("[DIR] "):
        item_name = item_name.replace("[DIR] ", "", 1)

    item_path = current_path / item_name

    try:
        stats = fileops.get_properties(item_path)

        size = stats.st_size
        modified = datetime.fromtimestamp(stats.st_mtime)
        created = datetime.fromtimestamp(stats.st_ctime)

        readable = "Yes" if item_path.exists() and item_path.is_file() else "N/A"
        writable = "Yes" if item_path.exists() else "N/A"

        messagebox.showinfo(
            "Properties",
            f"Name: {item_name}\n"
            f"Path: {item_path}\n"
            f"Size: {size} bytes\n"
            f"Created: {created}\n"
            f"Modified: {modified}\n"
            f"Directory: {item_path.is_dir()}\n"
            f"File: {item_path.is_file()}\n"
            f"Readable: {readable}\n"
            f"Writable: {writable}"
        )

        status_label.config(text=f"Showing properties for: {item_name}")

    except FileNotFoundError:
        status_label.config(text="File or folder not found")
    except PermissionError:
        status_label.config(text="Permission denied: cannot view properties")
    except Exception as e:
        status_label.config(text=f"Error showing properties: {str(e)}")

#-------------------------------------------------------
# --------------------- ALL BUTTONS -------------------------------------

button_frame = tk.Frame(window)
button_frame.pack(pady=12)


#--- Up Button ---
up_button = tk.Button(button_frame, text="Up One Folder", width=16, command=go_up_one_folder)
up_button.grid(row=0, column=0, padx=6, pady=6)


# --- Add Button ---
open_button = tk.Button(button_frame, text="Open File", width=16, command=open_selected_file)
open_button.grid(row=0, column=1, padx=6, pady=6)


# --- Save Button---
save_button = tk.Button(button_frame, text="Save Changes", width=16, command=save_selected_file)
save_button.grid(row=0, column=2, padx=6, pady=6)


# --- Create folder Button ---
create_folder_button = tk.Button(button_frame, text="Create Folder", width=16, command=create_folder)
create_folder_button.grid(row=1, column=1, padx=6, pady=6)


#--- Create File Button ---
create_button = tk.Button(button_frame, text="Create File", width=16, command=create_file)
create_button.grid(row=1, column=0, padx=6, pady=6)


# --- Delete Button ---
delete_button = tk.Button(button_frame, text="Delete Selected", width=16, command=delete_selected_item)
delete_button.grid(row=1, column=3, padx=6, pady=6)


# --- Remane Button ---
rename_button = tk.Button(button_frame, text="Rename Selected", width=16, command=rename_selected_item)
rename_button.grid(row=1, column=2, padx=6, pady=6)

# --- Properties button ---
properties_button = tk.Button(button_frame, text="Properties", width=16, command=show_properties)
properties_button.grid(row=2, column=0, columnspan=4, padx=6, pady=6)


# --- Refresh button ---
refresh_button = tk.Button(button_frame, text="Refresh", width=16, command=load_files)
refresh_button.grid(row=0, column=3, padx=6, pady=6)
# --------------------------------------------------------------------------



file_listbox.bind("<Double-Button-1>", open_selected_item)
#Load files
load_files()


# helper closing function
def on_close():
    window.destroy()
    window.quit()

window.protocol("WM_DELETE_WINDOW", on_close)

# Run app
window.mainloop()