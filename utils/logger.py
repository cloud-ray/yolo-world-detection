# utils/logger.py
import os
import logging
from utils.config import LOG_DIRECTORY, LOG_FILE_NAME

def setup_logging(log_directory=LOG_DIRECTORY, log_filename=LOG_FILE_NAME):
    """
    Set up logging configuration.

    Args:
        log_directory (str): Directory where log files will be saved.
        log_filename (str): Name of the log file.

    Creates the log directory if it does not exist and configures logging to both 
    a file and the console. The log level is set to DEBUG for detailed logs.
    """
    # Ensure the log directory exists
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Define the log file path
    log_file_path = os.path.join(log_directory, log_filename)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG for detailed logs
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file_path),
                            logging.StreamHandler()  # Optionally also log to console
                        ])
