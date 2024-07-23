# functions/labeler.py

# Standard library imports
import sqlite3
import os
import logging

# Third-party library imports
from pybboxes import BoundingBox

# Project-specific imports
from utils.config import (
    SQLITE_DATABASE_PATH,
    ORIGINAL_SCREENSHOT_DIRECTORY,
    ORIGINAL_LABELS_DIRECTORY,
    RESIZED_LABELS_DIRECTORY,
    RESIZED_WITHOUT_BBOX_DIRECTORY
)
from utils.logger import setup_logging

# Set up logging using the utility function
setup_logging()


def ensure_directory_exists(directory):
    """Ensure that a directory exists, create it if it does not."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def update_database_with_yolo_labels(record_id, yolo_label_orig, yolo_label_resized):
    """
    Update the database with YOLO labels for the given record ID.

    Args:
        record_id (int): The ID of the record to update.
        yolo_label_orig (str): YOLO label for the original image.
        yolo_label_resized (str): YOLO label for the resized image.
    """
    try:
        with sqlite3.connect(SQLITE_DATABASE_PATH) as conn:
            cursor = conn.cursor()
            orig_class_id, orig_x_center, orig_y_center, orig_width, orig_height = map(float, yolo_label_orig.split())
            resized_class_id, resized_x_center, resized_y_center, resized_width, resized_height = map(float, yolo_label_resized.split())

            cursor.execute("""
                UPDATE screenshots
                SET orig_x_center = ?, orig_y_center = ?, orig_width = ?, orig_height = ?,
                    resized_x_center = ?, resized_y_center = ?, resized_width = ?, resized_height = ?
                WHERE id = ?
            """, (
                orig_x_center, orig_y_center, orig_width, orig_height,
                resized_x_center, resized_y_center, resized_width, resized_height,
                record_id
            ))

            conn.commit()
            logging.info(f"Database updated for record ID: {record_id}")

    except sqlite3.DatabaseError as e:
        logging.error(f"SQLite error while updating YOLO data: {e}")

def create_voc_bbox(x1, y1, x2, y2, image_size):
    """
    Create a VOC bounding box from coordinates and image size.

    Args:
        x1 (float): X-coordinate of the top-left corner.
        y1 (float): Y-coordinate of the top-left corner.
        x2 (float): X-coordinate of the bottom-right corner.
        y2 (float): Y-coordinate of the bottom-right corner.
        image_size (tuple): The size of the image as (width, height).

    Returns:
        BoundingBox: The created VOC bounding box.
    """
    return BoundingBox.from_voc(x1, y1, x2, y2, image_size=image_size)

def convert_voc_to_yolo(voc_bbox):
    """
    Convert a VOC bounding box to YOLO format.

    Args:
        voc_bbox (BoundingBox): The VOC bounding box to convert.

    Returns:
        BoundingBox: The converted YOLO bounding box.
    """
    return voc_bbox.to_yolo()

def create_yolo_label(class_id, yolo_bbox):
    """
    Create a YOLO label string from class ID and YOLO bounding box.

    Args:
        class_id (int): The class ID for the object.
        yolo_bbox (BoundingBox): The YOLO bounding box.

    Returns:
        str: The YOLO label as a string.
    """
    x_center, y_center, width, height = yolo_bbox.values
    return f"{class_id} {x_center} {y_center} {width} {height}"

def create_label_file_path(image_path, original=True):
    """
    Create the file path for the label file based on image path and type.

    Args:
        image_path (str): The path of the image.
        original (bool): Whether the image is original or resized.

    Returns:
        str: The path for the label file.
    """
    if original:
        return image_path.replace(".png", ".txt").replace(ORIGINAL_SCREENSHOT_DIRECTORY, ORIGINAL_LABELS_DIRECTORY)
    else:
        return image_path.replace(".jpg", ".txt").replace(RESIZED_WITHOUT_BBOX_DIRECTORY, RESIZED_LABELS_DIRECTORY)

def save_yolo_label_to_file(label_file_path, yolo_label):
    """
    Save the YOLO label to a file.

    Args:
        label_file_path (str): The path to the label file.
        yolo_label (str): The YOLO label string.
    """
    with open(label_file_path, "w") as f:
        f.write(yolo_label)

def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
    """
    Process and save YOLO labels for both original and resized images, and update the database.

    Args:
        record_id (int): The record ID for database update.
        class_id (int): The class ID of the object.
        x1, y1, x2, y2 (float): Bounding box coordinates for the original image.
        orig_shape_height, orig_shape_width (int): Shape of the original image.
        resized_x1, resized_y1, resized_x2, resized_y2 (float): Bounding box coordinates for the resized image.
        resized_shape_height, resized_shape_width (int): Shape of the resized image.
        screenshot_path (str): Path to the original screenshot.
        resized_image_path (str): Path to the resized image.
    """
    logging.info(f"Processing record ID: {record_id}")

    ensure_directory_exists(ORIGINAL_LABELS_DIRECTORY)
    ensure_directory_exists(RESIZED_LABELS_DIRECTORY)

    try:
        # Helper function to process and save labels
        def process_image_labels(x1, y1, x2, y2, image_size, label_path, class_id):
            voc_bbox = create_voc_bbox(x1, y1, x2, y2, image_size=image_size)
            yolo_bbox = convert_voc_to_yolo(voc_bbox)
            yolo_label = create_yolo_label(class_id, yolo_bbox)
            save_yolo_label_to_file(label_path, yolo_label)
            return yolo_label

        # Process and save labels for original image
        label_file_path_orig = create_label_file_path(screenshot_path)
        yolo_label_orig = process_image_labels(x1, y1, x2, y2, (orig_shape_width, orig_shape_height), label_file_path_orig, class_id)
        logging.info(f"YOLO label saved to: {label_file_path_orig}")

        # Process and save labels for resized image
        label_file_path_resized = create_label_file_path(resized_image_path, original=False)
        yolo_label_resized = process_image_labels(resized_x1, resized_y1, resized_x2, resized_y2, (resized_shape_width, resized_shape_height), label_file_path_resized, class_id)
        logging.info(f"YOLO label saved to: {label_file_path_resized}")

        # Update database with YOLO labels
        update_database_with_yolo_labels(record_id, yolo_label_orig, yolo_label_resized)

    except Exception as e:
        logging.error(f"Error processing record ID: {record_id} - {str(e)}")
