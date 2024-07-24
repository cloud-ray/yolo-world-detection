# stream_handler.py

import cv2
import logging
from utils.logger import setup_logging

setup_logging()

def initialize_stream(source):
    """
    Initialize a video stream from the specified source using OpenCV.

    Args:
        source (str): The source of the video stream (e.g., IP camera URL).

    Returns:
        cv2.VideoCapture: Initialized VideoCapture object if successful, otherwise None.
    """
    try:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            logging.error(f"Error opening video stream: {source}")
            return None
        logging.info(f"Stream initialized successfully with source: {source}")
        return cap
    except Exception as e:
        logging.error(f"Error initializing stream: {e}")
        return None