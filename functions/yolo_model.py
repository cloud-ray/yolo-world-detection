# functions/yolo_model.py
import logging
from ultralytics import YOLO
from utils.logger import setup_logging

# Set up logging
setup_logging()

def initialize_model(model_path, classes):
    """
    Initialize the YOLO model with the specified path and classes.

    Args:
        model_path (str): The path to the YOLO model file.
        classes (list): List of class names to set for the model.

    Returns:
        YOLO: Initialized YOLO model if successful, otherwise None.
    """
    try:
        model = YOLO(model_path)
        model.set_classes(classes)
        logging.info(f"Model initialized successfully with path: {model_path}")
        return model
    except Exception as e:
        logging.error(f"Error initializing model: {e}")
        return None
