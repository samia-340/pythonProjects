import json
from pathlib import Path

def load_config(config_path: str) -> dict:
    """Load configuration from a JSON file."""
    with open(config_path, 'r') as file:
        return json.load(file)

def get_default_directory(config: dict) -> Path:
    """Get the default directory from the configuration."""
    return Path(config.get("default_directory", "~")).expanduser()

def get_archive_directory(config: dict) -> Path:
    """Get the archive directory from the configuration."""
    return Path(config.get("archive_directory", "~")).expanduser()



# config_path = r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\configFile.json'

# # Load the configuration
# config = load_config(config_path)

# # Get directories
# default_dir = get_default_directory(config)
# archive_dir = get_archive_directory(config)

# print(f"Default Directory: {default_dir}")
# print(f"Archive Directory: {archive_dir}")