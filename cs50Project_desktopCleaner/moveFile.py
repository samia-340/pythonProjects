import os
import shutil

def move_files(source_dir, destination_dir):
    # Ensure the source and destination directories exist
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Destination directory '{destination_dir}' created.")

    # Iterate over all the files in the source directory
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)

        # Check if it's a file (not a directory) before moving
        if os.path.isfile(source_file):
            shutil.move(source_file, destination_file)
            print(f"Moved: {source_file} -> {destination_file}")

if __name__ == "__main__":
    source_directory = r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\sourcedir'  # path of the source directory path
    destination_directory = r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\destinationdir'  # path of the destination directory path

    move_files(source_directory,destination_directory)