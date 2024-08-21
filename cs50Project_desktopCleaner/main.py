import logging as log
from cleaner import DesktopCleaner
#from db_utils import create_activity_log_table, insert_activity_log, fetch_activity_summary

def main() -> None:
    log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    #this function is called to setup the logging system or to configure the logging
   
    config_path =  r'C:\Users\Dell\Desktop\pythonProjects\cs50Project_desktopCleaner\configFile.json'  # Path to the json configuration file
    
    cleaner = DesktopCleaner(config_path) # Create the instance of the class with path of configuration file
    
    cleaner.cleanup()  # Call the main class function
    cleaner.generate_summary()  # Generate and display the summary
    cleaner.close_connection()

if __name__ == "__main__":
    main()