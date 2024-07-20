# functions/screenshot_handler.py
import os
import time
import cv2
import logging
from utils.config import FRAME_COUNT_THRESHOLD, ADDITIONAL_FRAME_THRESHOLD, IMAGE_DIRECTORY, LABEL_DIRECTORY, SS_CONFIDENCE_THRESHOLD, MAX_SCREENSHOTS
from utils.logger import setup_logging
from functions.object_tracker import object_tracker, log_object_tracker_summary

# Set up logging using the utility function
setup_logging()

def save_label_file(file_path, class_idx, center_x, center_y, box_width, box_height):
    """
    Save the label information for an object detection to a file.

    Args:
        file_path (str): Path to the label file.
        class_idx (int): Class index of the detected object.
        center_x (float): X coordinate of the object's center in YOLO format.
        center_y (float): Y coordinate of the object's center in YOLO format.
        box_width (float): Width of the bounding box in YOLO format.
        box_height (float): Height of the bounding box in YOLO format.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(f"{class_idx} {center_x} {center_y} {box_width} {box_height}")
        logging.info(f"Label file saved: {file_path}")
    except Exception as e:
        logging.error(f"Error saving label file {file_path}: {e}")

def save_screenshot_and_label(obj_id, class_name, class_id, confidence, frame, timestamp, class_idx, center_x, center_y, box_width, box_height):
    """
    Save a screenshot and corresponding label file.

    Args:
        obj_id (int): The ID of the object being tracked.
        class_name (str): Name of the class of the detected object.
        class_id (int): ID of the class of the detected object.
        confidence (float): Confidence score of the detected object.
        frame (numpy.ndarray): The image frame containing the detected object.
        timestamp (int): Current timestamp for file naming.
        class_idx (int): Class index of the detected object.
        center_x (float): X coordinate of the object's center in YOLO format.
        center_y (float): Y coordinate of the object's center in YOLO format.
        box_width (float): Width of the bounding box in YOLO format.
        box_height (float): Height of the bounding box in YOLO format.
    """
    try:
        # Create directories if they don't exist
        os.makedirs(IMAGE_DIRECTORY, exist_ok=True)
        os.makedirs(LABEL_DIRECTORY, exist_ok=True)

        # Save the screenshot
        screenshot_path = f"{IMAGE_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.png"
        cv2.imwrite(screenshot_path, frame)
        logging.info(f"Screenshot saved: {screenshot_path}")

        # Save the corresponding label file
        label_file_path = f"{LABEL_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.txt"
        save_label_file(label_file_path, class_idx, center_x, center_y, box_width, box_height)
    except Exception as e:
        logging.error(f"Error saving screenshot or label file for object {obj_id}: {e}")

def check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height):
    """
    Check if a screenshot should be saved based on object tracking data and thresholds.
    Save the initial screenshot and corresponding label file if the conditions are met.
    Additionally, save extra screenshots if enough frames have passed since the last save.

    Args:
        obj_id (int): The ID of the object being tracked.
        class_idx (int): Class index of the detected object.
        confidence (float): Confidence score of the detected object.
        frame (numpy.ndarray): The image frame containing the detected object.
        classes (list): List of class names.
        center_x (float): X coordinate of the object's center in YOLO format.
        center_y (float): Y coordinate of the object's center in YOLO format.
        box_width (float): Width of the bounding box in YOLO format.
        box_height (float): Height of the bounding box in YOLO format.
    """
    class_name = classes[class_idx]
    class_id = class_idx
    timestamp = int(time.time())

    if obj_id in object_tracker:
        obj_data = object_tracker[obj_id]
        
        # Log summary before saving the screenshot
        if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
            log_object_tracker_summary(obj_id)  # Log the summary when saving the screenshot
            
        # Debug statements to check values
        logging.debug(f"Object ID: {obj_id}")
        logging.debug(f"Current confidence: {confidence}")
        logging.debug(f"Threshold: {SS_CONFIDENCE_THRESHOLD}")
        logging.debug(f"Object data: {obj_data}")

        # Check if the object has been tracked long enough and confidence is consistently high
        if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
            if confidence > SS_CONFIDENCE_THRESHOLD:
                if not obj_data['initial_saved']:
                    # Save the initial screenshot
                    save_screenshot_and_label(obj_id, class_name, class_id, confidence, frame, timestamp, class_idx, center_x, center_y, box_width, box_height)
                    obj_data['initial_saved'] = True
                    obj_data['screenshot_count'] = 1  # Initialize screenshot count
                    logging.info(f"Initial screenshot saved for object {obj_id}.")
                else:
                    # Save additional screenshots if enough frames have passed and max screenshots not reached
                    if obj_data['frames_since_last_screenshot'] >= ADDITIONAL_FRAME_THRESHOLD and obj_data['screenshot_count'] < MAX_SCREENSHOTS:
                        save_screenshot_and_label(obj_id, class_name, class_id, confidence, frame, timestamp, class_idx, center_x, center_y, box_width, box_height)
                        obj_data['frames_since_last_screenshot'] = 0
                        obj_data['screenshot_count'] += 1  # Increment screenshot count
                        logging.info(f"Additional screenshot saved for object {obj_id}.")
                    elif obj_data['screenshot_count'] >= MAX_SCREENSHOTS:
                        # Stop tracking the object if max screenshots are reached
                        obj_data['track'] = False
                        logging.info(f"Max screenshots reached for object {obj_id}. Stopping tracking.")
            else:
                obj_data['frames_since_last_screenshot'] = 0
    else:
        logging.warning(f"Object ID {obj_id} not found in tracker.")
