import os
import shutil

# Define the source directory, filename, and destination directory
source_dir = r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\sourcedir'
filename = 'srctext1.txt'
destination_dir = r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\destinationdir'

# Join the directory and filename to create the full paths
source_file = os.path.join(source_dir, filename)
destination_file = os.path.join(destination_dir, filename)

# Print the source and destination file paths
print(f"Source file: {source_file}")
print(f"Destination file: {destination_file}")

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Move the file
if os.path.isfile(source_file):
    shutil.move(source_file, destination_file)
    print(f"Moved: {source_file} -> {destination_file}")
else:
    print(f"File {source_file} does not exist.")