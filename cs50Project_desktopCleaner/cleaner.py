import os
import shutil
import uuid
import sqlite3
from typing import Tuple
from pathlib import Path
from datetime import datetime
import logging 


log = logging.getLogger('cleaner')# Create a logger object named 'cleaner'
log.setLevel(logging.INFO)  # Adjust as needed
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()# Create a handler that will output log messages to the console
console_handler.setFormatter(formatter)
log.addHandler(console_handler)# Add the console handler to the logger
log.propagate = False # Prevent the logger from propagating messages to the root logger


# Attempt to import necessary functions from the config module
try:
    from config import load_config, get_default_directory, get_archive_directory
    log.info("Imports from config are successful!")
except ImportError as e:
    log.error(f"ImportError: {e}")
# Attempt to import necessary functions from the db_utils module
try:
    from db_utils import create_activity_log_table, insert_activity_log, fetch_activity_summary
    log.info("Imports from db_utils are successful!")
except ImportError as e:
    log.error(f"ImportError: {e}")

class DesktopCleaner:
    def __init__(self, config_path: str) -> None:
        self._config_path = config_path  #path to json configuration file
        self._session_id = str(uuid.uuid4())  # Generate a unique session ID for the instance using UUID4 and store it as a string
        self._load_configuration()   # Load the configuration from the JSON file
        self._initialize_database()  # Initialize the database connection and set up the activity log tabl

    def _load_configuration(self) -> None:
        # Load the configuration from the JSON file into config which is a dictionary type.
        #This function is called from the config module
        config = load_config(self._config_path)
        self._source_dir = get_default_directory(config)
        self._retention_policy_days = config.get("retention_days", 30)
         # Path to the destination folders
        self._destinations = {
            "documents": self._source_dir / "Documents",
            "images": self._source_dir / "Pictures",
            "videos": self._source_dir / "Videos",
            "archives": get_archive_directory(config)
        }
        # Using get helps avoid KeyError exceptions that occur when accessing a key directly if it is not present in the dictionary.
        #default value is used
        self._doc_supported_ext = config.get("document_extensions", [])
        self._image_supported_ext = config.get("image_extensions", [])
        self._vid_supported_ext = config.get("video_extensions", [])
        self._excluded_extensions = config.get("excluded_extensions", [])
        self._db_name = config.get("database_name", 'desktop_cleaner.db')  # Name of the database used for logging

    def _initialize_database(self) -> None:
        # Establish a connection to the SQLite database using the specified database name
        self._conn = sqlite3.connect(self._db_name)
        # Create the activity_log table in the database if it does not already exis
        create_activity_log_table(self._conn)

    def is_file_old(self, file_path: Path) -> bool:
        # Get the file's access time
        file_access_time = os.path.getatime(file_path)
        file_access_date = datetime.fromtimestamp(file_access_time)
        return (datetime.now() - file_access_date).days >= self._retention_policy_days
    # this function calls the function of db_utils module to log the activity in db
    def log_activity(self, action: str, source: Path, destination: Path) -> None:
        try:
            insert_activity_log(self._conn, self._session_id, action, str(source), str(destination))
        except sqlite3.Error as e:
            log.error(f"Database error: {e}")
    #this function makes sure the existance of destination folders
    def prepare_folders(self) -> None:
        for folder in self._destinations.values():
            os.makedirs(folder, exist_ok=True)

    def move_file(self, source_file: Path, destination: Path) -> None:
        try:
            shutil.move(source_file, destination)
            self.log_activity(f"Moved to {destination.name.lower()}", source_file, destination)
        except Exception as e:
            log.error(f"Error moving file {source_file}: {e}")

    def cleanup(self) -> None:
        """Cleans up the desktop by moving files according to the configured rules."""
        # Check if the source directory exists, if not then raise an exception
        if not os.path.exists(self._source_dir):
            raise Exception(f"Source directory '{self._source_dir}' does not exist.")
        
        self.prepare_folders()

        # Loop through files in the source directory
        for filename in os.listdir(self._source_dir):
            source_file = os.path.join(self._source_dir, filename)  # Create full path for the file in consideration
            
            # Check if it is a file (not a directory)
            if os.path.isfile(source_file):
                # Get the extension
                _, file_extension = os.path.splitext(source_file)
                # Check if the extension is not excluded 
                if file_extension not in self._excluded_extensions:
                    # Check if the file is old
                    if self.is_file_old(source_file):
                        self.move_file(source_file, self._destinations["archives"])
                    else:
                        # If the file is frequently accessed, organize it in respective folders
                        if file_extension in self._doc_supported_ext:
                            self.move_file(source_file, self._destinations["documents"])
                        elif file_extension in self._image_supported_ext:
                            self.move_file(source_file, self._destinations["images"])
                        elif file_extension in self._vid_supported_ext:
                            self.move_file(source_file, self._destinations["videos"])

    def generate_summary(self) -> Tuple:
        """Generates a summary of the cleanup operation."""
        activities=fetch_activity_summary(self._conn,self._session_id)
        log.info("Summary of Activities:")
        log.info("Action Counts:")
        log.debug(f"Activities[0]: {activities[0]}")
        for action, count in activities[0]:  # Display counts of actions
            #print(f"{action}: {count} times")
            log.info(f"{action}: {count} times")

        
        print("\nRecent Actions:")
        # Loop through to display detailed summary
        for timestamp, action, source, destination in activities[1]:
            #print(f"{timestamp} - {action}: {source} -> {destination}")
            log.info(f"{timestamp} - {action}: {source} -> {destination}")
        return activities   

    def close_connection(self) -> None:
        """Closes the database connection."""
        if self._conn:
            self._conn.close()

# Ensure to close the connection after operations
if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    config_path = r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\configFile.json'
    cleaner = DesktopCleaner(config_path)
    try:
        cleaner.cleanup()
        cleaner.generate_summary()
    finally:
        cleaner.close_connection()