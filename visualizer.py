import os

def get_py_files(directory):
    py_file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_file_list.append(file)
    return py_file_list

def display_files(file_list):
    for i, file in enumerate(file_list):
        file_name = os.path.splitext(file)[0]
        print(f"{i+1}. {file_name}")

def select_file(file_list):
    while True:
        try:
            choice = int(input("Enter the number corresponding to the file you want to import (or 0 to exit): "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(file_list):
                return file_list[choice-1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def import_file(file_path):
    try:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        exec(f"from graphs import {module_name}")
    except Exception as e:
        print(f"Error importing file: {e}")

directory = "graphs"
py_files = get_py_files(directory)
if len(py_files) == 0:
    print("No Python files found in the directory.")
else:
    print("Available options:")
    display_files(py_files)
    selected_file = select_file(py_files)
    if selected_file is None:
        print("No file selected.")
    else:
        print(f"Selected file: {selected_file}")
        import_file(os.path.join(directory, selected_file))
