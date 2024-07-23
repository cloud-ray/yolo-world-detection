# functions/screenshot_handler.py

# Standard library imports
import time

# Third-party library imports
import cv2
import logging
import sqlite3

# Project-specific imports
from functions.object_tracker import (
    object_tracker,
    log_object_tracker_summary
)
from functions.screenshot_resizer import resize_screenshot

# Utility imports
from utils.logger import setup_logging

# Configuration imports
from utils.config import (
    FRAME_COUNT_THRESHOLD,
    ADDITIONAL_FRAME_THRESHOLD,
    ORIGINAL_SCREENSHOT_DIRECTORY,
    SS_CONFIDENCE_THRESHOLD,
    SQLITE_DATABASE_PATH
)


# Set up logging using the utility function
setup_logging()


def generate_screenshot_path(class_name, class_id, confidence, obj_id, timestamp):
    """Generates a formatted path for saving screenshots."""
    return f"{ORIGINAL_SCREENSHOT_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.png"

def check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, x1, y1, x2, y2, orig_shape):
    """
    Checks if the conditions are met to save a screenshot and its details to the database.

    Parameters:
        obj_id (int): The ID of the object.
        class_idx (int): The index of the object's class.
        confidence (float): The confidence score of the detection.
        frame (np.array): The image frame containing the object.
        classes (list): The list of class names.
        x1, y1, x2, y2 (int): Bounding box coordinates.
        orig_shape (tuple): The original shape of the image (width, height).
    """
    class_name = classes[class_idx]
    class_id = class_idx
    timestamp = int(time.time())

    if not orig_shape:
        logging.error("orig_shape is not provided")
        return

    orig_shape_width, orig_shape_height = orig_shape
    logging.debug(f"orig_shape_width: {orig_shape_width}, orig_shape_height: {orig_shape_height}")

    if obj_id in object_tracker:
        obj_data = object_tracker[obj_id]

        if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
            log_object_tracker_summary(obj_id)

        logging.info(f"Object ID: {obj_id}")
        logging.info(f"Current confidence: {confidence}")
        logging.info(f"Threshold: {SS_CONFIDENCE_THRESHOLD}")
        logging.info(f"Object data: Frame Count: {obj_data.get('frame_count', 'N/A')}, Frames Since Last Screenshot: {obj_data.get('frames_since_last_screenshot', 'N/A')}, Saved: {obj_data.get('saved', 'N/A')}")

        if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
            if confidence > SS_CONFIDENCE_THRESHOLD and not obj_data['saved']:
                screenshot_path = generate_screenshot_path(class_name, class_id, confidence, obj_id, timestamp)
                cv2.imwrite(screenshot_path, frame)
                logging.info(f"Screenshot saved: {screenshot_path}")

                save_to_db(class_name, class_id, confidence, obj_id, timestamp, screenshot_path, x1, y1, x2, y2, orig_shape_height, orig_shape_width, obj_data['frame_count'], obj_data['frames_since_last_screenshot'])

                obj_data['saved'] = True
                logging.info(f"Initial screenshot saved for {class_name}_{confidence:.2f}_{obj_id}.")

            if obj_data['frames_since_last_screenshot'] >= ADDITIONAL_FRAME_THRESHOLD:
                try:
                    additional_screenshot_path = generate_screenshot_path(class_name, class_id, confidence, obj_id, timestamp)
                    cv2.imwrite(additional_screenshot_path, frame)
                    logging.info(f"Additional screenshot for {class_name}_{confidence:.2f}_{obj_id} saved: {additional_screenshot_path}")

                    save_to_db(class_name, class_id, confidence, obj_id, timestamp, additional_screenshot_path, x1, y1, x2, y2, orig_shape_height, orig_shape_width, obj_data['frame_count'], obj_data['frames_since_last_screenshot'])
                except Exception as e:
                    logging.error(f"Error saving additional screenshot for object {obj_id}: {e}")

                obj_data['frames_since_last_screenshot'] = 0
                logging.info(f"Additional screenshot saved for {class_name}_{confidence:.2f}_{obj_id}.")
        else:
            logging.debug(f"Frame count {obj_data['frame_count']} is less than threshold {FRAME_COUNT_THRESHOLD}.")
    else:
        logging.warning(f"Object ID {obj_id} not found in tracker.")

def save_to_db(class_name, class_id, confidence, obj_id, timestamp, screenshot_path, x1, y1, x2, y2, orig_shape_height, orig_shape_width, frame_count, frames_since_last_screenshot):
    """
    Saves the screenshot details to the SQLite database and resizes the screenshot.

    Parameters:
        class_name (str): The name of the object's class.
        class_id (int): The ID of the object's class.
        confidence (float): The confidence score of the detection.
        obj_id (int): The ID of the object.
        timestamp (int): The timestamp when the screenshot was taken.
        screenshot_path (str): The file path where the screenshot is saved.
        x1, y1, x2, y2 (int): Bounding box coordinates.
        orig_shape_height, orig_shape_width (int): The original dimensions of the image.
        frame_count (int): The count of frames since the object was first detected.
        frames_since_last_screenshot (int): The count of frames since the last screenshot was taken.
    """
    try:
        logging.info("Connecting to SQLite database.")
        with sqlite3.connect(SQLITE_DATABASE_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO screenshots (class_name, class_id, confidence, obj_id, timestamp, screenshot_path, x1, y1, x2, y2, orig_shape_height, orig_shape_width, frame_count, frames_since_last_screenshot)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (class_name, class_id, confidence, obj_id, timestamp, screenshot_path, x1, y1, x2, y2, orig_shape_height, orig_shape_width, frame_count, frames_since_last_screenshot))

            record_id = cursor.lastrowid
            logging.info(f"Data successfully written to SQLite database for {class_name}_{confidence:.2f}_{obj_id}.")

        resize_screenshot(record_id, screenshot_path, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width)
    
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
