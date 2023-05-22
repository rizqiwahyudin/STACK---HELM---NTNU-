import os
import subprocess
import split_exported_xml

def get_files_in_folder(folder_path):
    files_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)
    return files_list

# Provide the folder path
folder_path = "xml\prettified"  # Replace with the actual folder path

# Get the list of files in the folder
files = get_files_in_folder(folder_path)

# Loop through the files and split them
for file in files:
    subprocess.run(["python", "xml/split_exported_xml.py", file])
