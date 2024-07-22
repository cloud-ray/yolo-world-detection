# functions/labeler.py
import sqlite3
import json
import os
import pybboxes as pbx
from utils.config import SQLITE_DATABASE_PATH
import logging
from utils.logger import setup_logging

# Set up logging using the utility function
setup_logging()

ORIGINAL_LABELS_DIRECTORY = "screenshots/original/labels"
RESIZED_LABELS_DIRECTORY = "screenshots/resized/labels"

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_yolo_label(file_path, class_id, x_center, y_center, width, height):
    print(f"Saving YOLO label to {file_path} with values: class_id={class_id}, x_center={x_center}, y_center={y_center}, width={width}, height={height}")
    with open(file_path, "w") as file:
        file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
    print(f"YOLO label saved to {file_path}")

def update_database_with_yolo(record_id, orig_yolo, resized_yolo):
    print(f"Updating database for record ID {record_id} with YOLO data: orig_yolo={orig_yolo}, resized_yolo={resized_yolo}")
    try:
        conn = sqlite3.connect(SQLITE_DATABASE_PATH)
        cursor = conn.cursor()
        
        # Unpack tuples for SQL query
        orig_x_center, orig_y_center, orig_width, orig_height = orig_yolo
        resized_x_center, resized_y_center, resized_width, resized_height = resized_yolo
        
        cursor.execute("""
        UPDATE screenshots
        SET orig_x_center = ?, orig_y_center = ?, orig_width = ?, orig_height = ?,
            resized_x_center = ?, resized_y_center = ?, resized_width = ?, resized_height = ?
        WHERE id = ?
        """, (orig_x_center, orig_y_center, orig_width, orig_height,
              resized_x_center, resized_y_center, resized_width, resized_height,
              record_id))
        
        conn.commit()
        print(f"Database updated for record ID {record_id}")
    except sqlite3.Error as e:
        logging.error(f"SQLite error while updating YOLO data: {e}")
    finally:
        conn.close()


def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape, screenshot_path):
    try:
        print(f"Processing and saving YOLO labels for record ID {record_id}")
        
        # Convert JSON strings to tuples
        print(f"Original shape JSON: {orig_shape}")
        orig_shape = tuple(json.loads(orig_shape))
        print(f"Converted original shape: {orig_shape}")
        
        print(f"Resized shape JSON: {resized_shape}")
        resized_shape = tuple(json.loads(resized_shape))
        print(f"Converted resized shape: {resized_shape}")
        
        # Convert original bounding box to YOLO format
        orig_yolo_bbox = pbx.convert_bbox((x1, y1, x2, y2), from_type="voc", to_type="yolo", image_size=orig_shape)
        print(f"Original YOLO bbox: {orig_yolo_bbox}")
        
        # Convert resized bounding box to YOLO format
        resized_yolo_bbox = pbx.convert_bbox((resized_x1, resized_y1, resized_x2, resized_y2), from_type="voc", to_type="yolo", image_size=resized_shape)
        print(f"Resized YOLO bbox: {resized_yolo_bbox}")
        
        # Save original YOLO label
        orig_label_path = os.path.join(ORIGINAL_LABELS_DIRECTORY, f"{os.path.splitext(os.path.basename(screenshot_path))[0]}.txt")
        ensure_directory_exists(ORIGINAL_LABELS_DIRECTORY)
        save_yolo_label(orig_label_path, class_id, *orig_yolo_bbox)
        
        # Save resized YOLO label
        resized_label_path = os.path.join(RESIZED_LABELS_DIRECTORY, f"{os.path.splitext(os.path.basename(screenshot_path))[0]}.txt")
        ensure_directory_exists(RESIZED_LABELS_DIRECTORY)
        save_yolo_label(resized_label_path, class_id, *resized_yolo_bbox)
        
        # Update the database with YOLO format data
        update_database_with_yolo(record_id, orig_yolo_bbox, resized_yolo_bbox)
    
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
