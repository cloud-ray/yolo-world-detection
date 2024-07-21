# functions/screenshot_handler.py
import os
import time
import cv2
import logging
import json
from utils.config import FRAME_COUNT_THRESHOLD, ADDITIONAL_FRAME_THRESHOLD, IMAGE_DIRECTORY, SS_CONFIDENCE_THRESHOLD
from utils.logger import setup_logging
from functions.object_tracker import object_tracker, log_object_tracker_summary

# Set up logging using the utility function
setup_logging()


JSON_DIRECTORY = "screenshots/images/json"
JSON_FILE_NAME = "screenshot_data.json"

def save_additional_screenshot(obj_id, class_idx, confidence, frame, classes, timestamp):
    """
    Save an additional screenshot without label file.

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
        timestamp (int): Current timestamp for file naming.

    This function creates directories for storing images if they do not exist. 
    It saves an additional screenshot in the specified directory.
    """
    try:
        # Create directory if it doesn't exist
        image_dir = IMAGE_DIRECTORY
        os.makedirs(image_dir, exist_ok=True)

        class_name = classes[class_idx]
        class_id = class_idx
        timestamp = int(time.time())

        # Save additional screenshot
        # screenshot_path = f"{image_dir}/{classes[class_idx]}_{class_idx}_{confidence:.2f}_{obj_id}_{timestamp}.png"
        screenshot_path = f"{IMAGE_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.png"
        cv2.imwrite(screenshot_path, frame)
        logging.info(f"Additional screenshot saved: {screenshot_path}")
    except Exception as e:
        logging.error(f"Error saving additional screenshot for object {obj_id}: {e}")

def check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height, x1, y1, x2, y2, orig_shape):
    # print("check_and_save_screenshot called with arguments:", obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height, x1, y1, x2, y2, orig_shape)
    # def check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height, xyxy, conf, cls, ids, orig_shape, x1, y1, x2, y2):
    """
    Check if a screenshot should be saved based on object tracking data and thresholds.
    Save the initial screenshot if the conditions are met. 
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
            log_object_tracker_summary(obj_id)

        # Debug statements to check values
        logging.debug(f"Object ID: {obj_id}")
        logging.debug(f"Current confidence: {confidence}")
        logging.debug(f"Threshold: {SS_CONFIDENCE_THRESHOLD}")
        logging.debug(f"Object data: Frame Count: {obj_data.get('frame_count', 'N/A')}, Frames Since Last Screenshot: {obj_data.get('frames_since_last_screenshot', 'N/A')}, Saved: {obj_data.get('saved', 'N/A')}")

        # Check if the object has been tracked long enough and confidence is consistently high
        if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
            if confidence > SS_CONFIDENCE_THRESHOLD and not obj_data['saved']:
                # Ensure the directory exists
                os.makedirs(IMAGE_DIRECTORY, exist_ok=True)
                os.makedirs(JSON_DIRECTORY, exist_ok=True)

                # Define json_filename and path
                json_filename = JSON_FILE_NAME
                json_path = os.path.join(JSON_DIRECTORY, json_filename)

                # Save the initial screenshot with obj_id included in the filename
                screenshot_path = f"{IMAGE_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.png"
                cv2.imwrite(screenshot_path, frame)
                logging.info(f"Screenshot saved: {screenshot_path}")

                # Save screenshot path and bounding box information to a JSON file
                save_to_json(json_path, screenshot_path, x1, y1, x2, y2, orig_shape)

                object_tracker[obj_id]['saved'] = True  # Mark as saved
                logging.info(f"Initial screenshot saved for object {obj_id}.")

            # Call the function to save additional screenshots if enough frames have passed
            if obj_data['frames_since_last_screenshot'] >= ADDITIONAL_FRAME_THRESHOLD:
                save_additional_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height, timestamp)
                obj_data['frames_since_last_screenshot'] = 0  # Reset the counter
                logging.info(f"Additional screenshot saved for object {obj_id}.")
        else:
            logging.debug(f"Frame count {obj_data['frame_count']} is less than threshold {FRAME_COUNT_THRESHOLD}.")
    else:
        logging.warning(f"Object ID {obj_id} not found in tracker.")



def save_to_json(json_path, screenshot_path, x1, y1, x2, y2, orig_shape):
    # Create the JSON data to be appended
    new_data = {
        "image_path": screenshot_path,
        "bbox": {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        },
        "orig_shape": orig_shape
    }

    # Check if the JSON file already exists
    if os.path.exists(json_path):
        # Read existing data
        with open(json_path, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        # Create a new list if the file does not exist
        existing_data = {"objects": []}

    # Append new data
    existing_data["objects"].append(new_data)

    # Write updated data back to the JSON file
    with open(json_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
    
    logging.info(f"JSON data saved: {json_path}")





# # WORKS WITH LABEL
#         def save_label_file(file_path, class_idx, center_x, center_y, box_width, box_height):
#     """
#     Save the label information for an object detection to a file.

#     Args:
#         file_path (str): Path to the label file.
#         class_idx (int): Class index of the detected object.
#         center_x (float): X coordinate of the object's center in YOLO format.
#         center_y (float): Y coordinate of the object's center in YOLO format.
#         box_width (float): Width of the bounding box in YOLO format.
#         box_height (float): Height of the bounding box in YOLO format.
#     """
#     try:
#         with open(file_path, 'w') as file:
#             file.write(f"{class_idx} {center_x} {center_y} {box_width} {box_height}")
#         logging.info(f"Label file saved: {file_path}")
#     except Exception as e:
#         logging.error(f"Error saving label file {file_path}: {e}")

# def save_additional_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height, timestamp):
#     """
#     Save an additional screenshot and corresponding label file.

#     Args:
#         obj_id (int): The ID of the object being tracked.
#         class_idx (int): Class index of the detected object.
#         confidence (float): Confidence score of the detected object.
#         frame (numpy.ndarray): The image frame containing the detected object.
#         classes (list): List of class names.
#         center_x (float): X coordinate of the object's center in YOLO format.
#         center_y (float): Y coordinate of the object's center in YOLO format.
#         box_width (float): Width of the bounding box in YOLO format.
#         box_height (float): Height of the bounding box in YOLO format.
#         timestamp (int): Current timestamp for file naming.

#     This function creates directories for storing images and label files if they do not exist. 
#     It saves an additional screenshot and its corresponding label file in the specified directories. 
#     The paths for these directories are determined by `IMAGE_DIRECTORY` and `LABEL_DIRECTORY` constants.
#     """
#     try:
#         # Create directories if they don't exist
#         image_dir = IMAGE_DIRECTORY
#         label_dir = LABEL_DIRECTORY
#         os.makedirs(image_dir, exist_ok=True)
#         os.makedirs(label_dir, exist_ok=True)

#         # Save additional screenshot
#         screenshot_path = f"{image_dir}/{classes[class_idx]}_{class_idx}_{confidence:.2f}_{obj_id}_{timestamp}.png"
#         cv2.imwrite(screenshot_path, frame)
#         logging.info(f"Additional screenshot saved: {screenshot_path}")

#         # Save corresponding label file
#         label_file_path = f"{label_dir}/{classes[class_idx]}_{class_idx}_{confidence:.2f}_{obj_id}_{timestamp}.txt"
#         save_label_file(label_file_path, class_idx, center_x, center_y, box_width, box_height)
#     except Exception as e:
#         logging.error(f"Error saving additional screenshot or label file for object {obj_id}: {e}")


# def check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height):
#     """
#     Check if a screenshot should be saved based on object tracking data and thresholds.
#     Save the initial screenshot and corresponding label file if the conditions are met.
#     Additionally, save extra screenshots if enough frames have passed since the last save.

#     Args:
#         obj_id (int): The ID of the object being tracked.
#         class_idx (int): Class index of the detected object.
#         confidence (float): Confidence score of the detected object.
#         frame (numpy.ndarray): The image frame containing the detected object.
#         classes (list): List of class names.
#         center_x (float): X coordinate of the object's center in YOLO format.
#         center_y (float): Y coordinate of the object's center in YOLO format.
#         box_width (float): Width of the bounding box in YOLO format.
#         box_height (float): Height of the bounding box in YOLO format.
#     """
#     class_name = classes[class_idx]
#     class_id = class_idx
#     timestamp = int(time.time())

#     if obj_id in object_tracker:
#         obj_data = object_tracker[obj_id]
        
#         # Log summary before saving the screenshot
#         if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
#             log_object_tracker_summary(obj_id)  # Log the summary when saving the screenshot
            
#         # Debug statements to check values
#         logging.debug(f"Object ID: {obj_id}")
#         logging.debug(f"Current confidence: {confidence}")
#         logging.debug(f"Threshold: {SS_CONFIDENCE_THRESHOLD}")
#         # logging.debug(f"Object data: {obj_data}")
#         logging.debug(f"Object data: Frame Count: {obj_data.get('frame_count', 'N/A')}, Frames Since Last Screenshot: {obj_data.get('frames_since_last_screenshot', 'N/A')}, Saved: {obj_data.get('saved', 'N/A')}")

#         # Check if the object has been tracked long enough and confidence is consistently high
#         if obj_data['frame_count'] >= FRAME_COUNT_THRESHOLD:
#             if confidence > SS_CONFIDENCE_THRESHOLD and not obj_data['saved']:
#                 # Ensure the directories exist
#                 os.makedirs(IMAGE_DIRECTORY, exist_ok=True)
#                 os.makedirs(LABEL_DIRECTORY, exist_ok=True)

#                 # Save the initial screenshot with obj_id included in the filename
#                 screenshot_path = f"{IMAGE_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.png"
#                 cv2.imwrite(screenshot_path, frame)
#                 logging.info(f"Screenshot saved: {screenshot_path}")

#                 # Save the corresponding label file
#                 label_file_path = f"{LABEL_DIRECTORY}/{class_name}_{class_id}_{confidence:.2f}_{obj_id}_{timestamp}.txt"
#                 save_label_file(label_file_path, class_idx, center_x, center_y, box_width, box_height)

#                 object_tracker[obj_id]['saved'] = True  # Mark as saved
#                 logging.info(f"Label and initial screenshot saved for object {obj_id}.")
            
#             # Call the function to save additional screenshots if enough frames have passed
#             if obj_data['frames_since_last_screenshot'] >= ADDITIONAL_FRAME_THRESHOLD:
#                 save_additional_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height, timestamp)
#                 obj_data['frames_since_last_screenshot'] = 0  # Reset the counter
#                 logging.info(f"Additional screenshot saved for object {obj_id}.")
#         else:
#             logging.debug(f"Frame count {obj_data['frame_count']} is less than threshold {FRAME_COUNT_THRESHOLD}.")
#     else:
#         logging.warning(f"Object ID {obj_id} not found in tracker.")
