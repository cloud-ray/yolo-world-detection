# stream_handler.py

# Third-party library imports
from vidgear.gears import CamGear

# Utility imports
import logging
from utils.logger import setup_logging

# Set up logging
setup_logging()

def initialize_stream(source):
    """
    Initialize a video stream from the specified source using CamGear.

    Args:
        source (str): The source of the video stream (e.g., YouTube Live URL).

    Returns:
        CamGear: Initialized CamGear object if successful, otherwise None.
    """
    try:
        cap = CamGear(source=source, stream_mode=True, logging=True).start()
        logging.info(f"Stream initialized successfully with source: {source}")
        return cap
    except Exception as e:
        logging.error(f"Error initializing stream: {e}")
        return None
