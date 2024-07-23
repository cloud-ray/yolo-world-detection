# functions/screenshot_resizer.py

# Standard library imports
import os

# Third-party library imports
import cv2
import sqlite3
import logging

# Project-specific imports
from functions.labeler import process_and_save_yolo_labels

# Utility imports
from utils.logger import setup_logging

# Configuration imports
from utils.config import (
    SQLITE_DATABASE_PATH, IMAGE_QUALITY, NEW_IMAGE_SIZE_HEIGHT, NEW_IMAGE_SIZE_WIDTH,
    RESIZED_WITH_BBOX_DIRECTORY, RESIZED_WITHOUT_BBOX_DIRECTORY
)

# Set up logging using the utility function
setup_logging()


def ensure_directory_exists(directory):
    """Ensure that the specified directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        logging.info(f"Creating directory: {directory}")
        os.makedirs(directory)
    logging.debug(f"Directory exists: {directory}")

def resize_image(image, new_size):
    """Resize the input image to the specified dimensions using cv2."""
    if image is None:
        logging.error("Invalid image object. Cannot resize.")
        return None
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    logging.info(f"Image resized successfully to {new_size}")
    return resized_image

def save_image(image, path, image_quality):
    """Save the image to the specified path with the given quality."""
    if image is None:
        logging.error("Invalid image object. Cannot save.")
        return
    cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), image_quality])
    logging.info(f"Image saved successfully: {path}")

def draw_bounding_boxes(image, x1, y1, x2, y2):
    """Draw a bounding box on the image with the given coordinates."""
    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
    if image is not None and all(val >= 0 for val in (x1, y1, x2, y2)):
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        logging.info("Bounding box drawn successfully on image")
    else:
        logging.error("Invalid bounding box coordinates or image.")
    return image

def update_database(record_id, resized_image_path, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width):
    """Update the database with information about the resized image and bounding boxes."""
    try:
        with sqlite3.connect(SQLITE_DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE screenshots
            SET resized_screenshot_path = ?, resized_x1 = ?, resized_y1 = ?, resized_x2 = ?, resized_y2 = ?, resized_shape_height = ?, resized_shape_width = ?
            WHERE id = ?
            """, (resized_image_path, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, record_id))
            conn.commit()
            logging.info(f"Successfully updated resized data for record ID {record_id}.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error while updating resized data: {e}")

def resize_screenshot(record_id, screenshot_path, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width):
    """Resize the screenshot, draw bounding boxes, and update the database with resized details."""
    ensure_directory_exists(RESIZED_WITHOUT_BBOX_DIRECTORY)
    ensure_directory_exists(RESIZED_WITH_BBOX_DIRECTORY)

    image = cv2.imread(screenshot_path)
    if image is None:
        logging.error(f"Failed to read image from {screenshot_path}")
        return

    scale_x = NEW_IMAGE_SIZE_WIDTH / orig_shape_width
    scale_y = NEW_IMAGE_SIZE_HEIGHT / orig_shape_height

    resized_image = resize_image(image, (NEW_IMAGE_SIZE_WIDTH, NEW_IMAGE_SIZE_HEIGHT))
    if resized_image is None:
        return

    resized_image_path = os.path.join(RESIZED_WITHOUT_BBOX_DIRECTORY, f"{os.path.splitext(os.path.basename(screenshot_path))[0]}.jpg")
    save_image(resized_image, resized_image_path, IMAGE_QUALITY)

    resized_x1 = x1 * scale_x
    resized_y1 = y1 * scale_y
    resized_x2 = x2 * scale_x
    resized_y2 = y2 * scale_y

    resized_image_with_bbox = draw_bounding_boxes(resized_image.copy(), resized_x1, resized_y1, resized_x2, resized_y2)
    resized_image_path_with_bbox = os.path.join(RESIZED_WITH_BBOX_DIRECTORY, f"{os.path.splitext(os.path.basename(screenshot_path))[0]}_bbox.jpg")
    save_image(resized_image_with_bbox, resized_image_path_with_bbox, IMAGE_QUALITY)

    # Define resized shape dimensions
    resized_shape_height = NEW_IMAGE_SIZE_HEIGHT
    resized_shape_width = NEW_IMAGE_SIZE_WIDTH

    # Update the database with resized dimensions
    update_database(record_id, resized_image_path, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width)
    logging.info(f"Screenshot resizing and database update successful for record ID {record_id}.")

    process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path)
    logging.info(f"Screenshot processing, labeling, and database update completed for record ID {record_id}.")
