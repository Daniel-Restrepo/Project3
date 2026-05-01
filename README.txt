CS 3502 Project 3 - File System Implementation

Name: Daniel Restrepo
Language: Python
GUI Framework: Tkinter

Project Description:
This project is a simple graphical file manager built in Python. It allows users to create, read, update, delete, rename, and navigate files and folders using a GUI. The program uses actual operating system file operations through Python modules such as pathlib and built-in file handling.

Files Included:
main.py - Contains the Tkinter GUI and user interaction logic.
file_operations.py - Contains the file system operation functions.
test_files/ - Safe testing folder used by the application.
README.txt - Instructions for running the project.

How to Run:
1. Make sure Python 3 is installed.
2. Open the project folder in VS Code (or any IDE).
3. Open the terminal.
4. Run:

python main.py

Notes:
The program starts inside the test_files folder for safety. This prevents accidental changes to important system or personal files during testing.

Implemented Features:
- Create files
- Create folders
- Open and read files
- Edit and save file contents
- Rename files and folders
- Delete files and empty folders
- Navigate into folders
- Move up one folder
- Refresh file list
- View file/folder properties
- Display status and error messages

Testing:
The application was tested with basic CRUD operations, directory navigation, duplicate file creation, non-empty folder deletion, renaming, and metadata display.
