# functions/labeler.py
import sqlite3
import os
from pybboxes import BoundingBox
from utils.config import SQLITE_DATABASE_PATH
import logging
from utils.logger import setup_logging

# Set up logging using the utility function
setup_logging()

ORIGINAL_LABELS_DIRECTORY = "screenshots/original/labels"
RESIZED_LABELS_DIRECTORY = "screenshots/resized/labels"
ORIGINAL_SCREENSHOT_DIRECTORY = "screenshots/original/screenshots"
RESIZED_WITHOUT_BBOX_DIRECTORY = "screenshots/resized/without_bbox"

ORIGINAL_YOLO_CONFIRMATION_DIRECTORY = "screenshots/original/yolo_bbox"
RESIZED_YOLO_CONFIRMATION_DIRECTORY = "screenshots/resized/yolo_bbox"

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def update_database_with_yolo_labels(record_id, yolo_label_orig, yolo_label_resized):
    try:
        conn = sqlite3.connect(SQLITE_DATABASE_PATH)
        cursor = conn.cursor()

        # Extract values from YOLO labels
        orig_class_id, orig_x_center, orig_y_center, orig_width, orig_height = [float(x) for x in yolo_label_orig.split()]
        resized_class_id, resized_x_center, resized_y_center, resized_width, resized_height = [float(x) for x in yolo_label_resized.split()]

        # Update database with YOLO labels
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

    except sqlite3.Error as e:
        logging.error(f"SQLite error while updating YOLO data: {e}")
    finally:
        if conn:
            conn.close()

def create_voc_bbox(x1, y1, x2, y2, image_size):
    return BoundingBox.from_voc(x1, y1, x2, y2, image_size=image_size)

def convert_voc_to_yolo(voc_bbox):
    return voc_bbox.to_yolo()

def create_yolo_label(class_id, yolo_bbox):
    x_center, y_center, width, height = yolo_bbox.values
    return f"{class_id} {x_center} {y_center} {width} {height}"

def create_label_file_path(image_path, original=True):
    if original:
        return image_path.replace(".png", ".txt").replace(ORIGINAL_SCREENSHOT_DIRECTORY, ORIGINAL_LABELS_DIRECTORY)
    else:
        return image_path.replace(".jpg", ".txt").replace(RESIZED_WITHOUT_BBOX_DIRECTORY, RESIZED_LABELS_DIRECTORY)

def save_yolo_label_to_file(label_file_path, yolo_label):
    with open(label_file_path, "w") as f:
        f.write(yolo_label)

def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
    logging.info(f"Processing record ID: {record_id}")

    ensure_directory_exists(ORIGINAL_LABELS_DIRECTORY)
    ensure_directory_exists(RESIZED_LABELS_DIRECTORY)

    try:
        # Create a VOC bounding box for original image
        voc_bbox_orig = create_voc_bbox(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
        logging.debug(f"VOC bounding box created for original image: {voc_bbox_orig}")

        # Convert VOC bounding box to YOLO format for original image
        yolo_bbox_orig = convert_voc_to_yolo(voc_bbox_orig)
        logging.debug(f"YOLO bounding box created for original image: {yolo_bbox_orig}")

        # Create YOLO label with class_id for original image
        yolo_label_orig = create_yolo_label(class_id, yolo_bbox_orig)
        logging.debug(f"YOLO label created for original image: {yolo_label_orig}")

        # Create label file path for original image
        label_file_path_orig = create_label_file_path(screenshot_path)
        logging.debug(f"Label file path for original image: {label_file_path_orig}")

        # Save YOLO label to file for original image
        save_yolo_label_to_file(label_file_path_orig, yolo_label_orig)
        logging.info(f"YOLO label saved to: {label_file_path_orig}")

        # Create a VOC bounding box for resized image
        voc_bbox_resized = create_voc_bbox(resized_x1, resized_y1, resized_x2, resized_y2, image_size=(resized_shape_width, resized_shape_height))
        logging.debug(f"VOC bounding box created for resized image: {voc_bbox_resized}")

        # Convert VOC bounding box to YOLO format for resized image
        yolo_bbox_resized = convert_voc_to_yolo(voc_bbox_resized)
        logging.debug(f"YOLO bounding box created for resized image: {yolo_bbox_resized}")

        # Create YOLO label with class_id for resized image
        yolo_label_resized = create_yolo_label(class_id, yolo_bbox_resized)
        logging.debug(f"YOLO label created for resized image: {yolo_label_resized}")

        print(f"Resized image path: {resized_image_path}")
        label_file_path_resized = create_label_file_path(resized_image_path, original=False)
        logging.debug(f"Label file path for resized image: {label_file_path_resized}")

        # Save YOLO label to file for resized image
        save_yolo_label_to_file(label_file_path_resized, yolo_label_resized)
        logging.info(f"YOLO label saved to: {label_file_path_resized}")

        # Update database with YOLO labels
        update_database_with_yolo_labels(record_id, yolo_label_orig, yolo_label_resized)
        logging.info(f"YOLO labels saved to SQL Database")

    except Exception as e:
        logging.error(f"Error processing record ID: {record_id} - {str(e)}")















# def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
#     logging.info(f"Processing record ID: {record_id}")

#     try:
#         # Create a VOC bounding box for original image
#         voc_bbox_orig = BoundingBox.from_voc(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
#         logging.debug(f"VOC bounding box created for original image: {voc_bbox_orig}")

#         # Convert VOC bounding box to YOLO format for original image
#         yolo_bbox_orig = voc_bbox_orig.to_yolo()
#         logging.debug(f"YOLO bounding box created for original image: {yolo_bbox_orig}")

#         # Create YOLO label with class_id for original image
#         x_center, y_center, width, height = yolo_bbox_orig.values
#         yolo_label_orig = f"{class_id} {x_center} {y_center} {width} {height}"
#         logging.debug(f"YOLO label created for original image: {yolo_label_orig}")

#         # Create label file path for original image
#         label_file_path_orig = screenshot_path.replace(".png", ".txt").replace(ORIGINAL_SCREENSHOT_DIRECTORY, ORIGINAL_LABELS_DIRECTORY)
#         logging.debug(f"Label file path for original image: {label_file_path_orig}")

#         # Save YOLO label to file for original image
#         with open(label_file_path_orig, "w") as f:
#             f.write(yolo_label_orig)
#         logging.info(f"YOLO label saved to: {label_file_path_orig}")

#         # Create a VOC bounding box for resized image
#         voc_bbox_resized = BoundingBox.from_voc(resized_x1, resized_y1, resized_x2, resized_y2, image_size=(resized_shape_width, resized_shape_height))
#         logging.debug(f"VOC bounding box created for resized image: {voc_bbox_resized}")

#         # Convert VOC bounding box to YOLO format for resized image
#         yolo_bbox_resized = voc_bbox_resized.to_yolo()
#         logging.debug(f"YOLO bounding box created for resized image: {yolo_bbox_resized}")

#         # Create YOLO label with class_id for resized image
#         x_center, y_center, width, height = yolo_bbox_resized.values
#         yolo_label_resized = f"{class_id} {x_center} {y_center} {width} {height}"
#         logging.debug(f"YOLO label created for resized image: {yolo_label_resized}")

#         print(f"Resized image path: {resized_image_path}")
#         label_file_path_resized = resized_image_path.replace(".jpg", ".txt").replace(RESIZED_WITHOUT_BBOX_DIRECTORY, RESIZED_LABELS_DIRECTORY)
#         logging.debug(f"Label file path for resized image: {label_file_path_resized}")

#         # Save YOLO label to file for resized image
#         with open(label_file_path_resized, "w") as f:
#             f.write(yolo_label_resized)
#         logging.info(f"YOLO label saved to: {label_file_path_resized}")

#     except Exception as e:
#         logging.error(f"Error processing record ID: {record_id} - {str(e)}")






# # WORKS WITH ORIGINAL SCREENSHOT
# def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
#     logging.info(f"Processing record ID: {record_id}")

#     try:
#         # Create a VOC bounding box
#         voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
#         logging.debug(f"VOC bounding box created: {voc_bbox}")

#         # Convert VOC bounding box to YOLO format
#         yolo_bbox = voc_bbox.to_yolo()
#         logging.debug(f"YOLO bounding box created: {yolo_bbox}")

#         # Create YOLO label with class_id
#         x_center, y_center, width, height = yolo_bbox.values
#         yolo_label = f"{class_id} {x_center} {y_center} {width} {height}"
#         logging.debug(f"YOLO label created: {yolo_label}")

#         # Create label file path
#         label_file_path = screenshot_path.replace(".png", ".txt").replace(ORIGINAL_SCREENSHOT_DIRECTORY, ORIGINAL_LABELS_DIRECTORY)
#         logging.debug(f"Label file path: {label_file_path}")

#         # Save YOLO label to file
#         with open(label_file_path, "w") as f:
#             f.write(yolo_label)
#         logging.info(f"YOLO label saved to: {label_file_path}")

#     except Exception as e:
#         logging.error(f"Error processing record ID: {record_id} - {str(e)}")


























# # PRINT STATEMENTS TO CONFIRM ORIGINAL VALUES + ACCESS VOC_BBOX AND YOLO_BBOX
#     print()
#     print("##### ORIGINAL VALUES #####")
#     print("x1:", x1)
#     print("y1:", y1)
#     print("x2:", x2)
#     print("y2:", y2)
#     print("orig_shape_width:", orig_shape_width)
#     print("orig_shape_height:", orig_shape_height)
#     print()

#     # Create a VOC bounding box
#     voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
#     print()
#     print("##### VOC VALUES #####")
#     print(dir(voc_bbox))
#     print()
#     print("VOC Bounding Box: ", voc_bbox)
#     print("raw_values: ", voc_bbox.raw_values)
#     print("image_size: ", voc_bbox.image_size)
#     print("values: ", voc_bbox.values)
#     print("x_br: ", voc_bbox.x_br)
#     print("x_tl: ", voc_bbox.x_tl)
#     print("y_br: ", voc_bbox.y_br)
#     print("y_tl: ", voc_bbox.y_tl)
#     print()

#     # Convert VOC bounding box to YOLO format
#     yolo_bbox = voc_bbox.to_yolo()
#     print()
#     print("##### YOLO VALUES #####")
#     print(dir(yolo_bbox))
#     print()
#     print("YOLO Bounding Box: ", yolo_bbox)
#     print("raw_values: ", yolo_bbox.raw_values)
#     print("image_size: ", yolo_bbox.image_size)
#     print("values: ", yolo_bbox.values)
#     print("x_br: ", yolo_bbox.x_br)
#     print("x_tl: ", yolo_bbox.x_tl)
#     print("y_br: ", yolo_bbox.y_br)
#     print("y_tl: ", yolo_bbox.y_tl)
#     print()





# YOLO_BBOX PLOTTING FOR YOLO VALUE CONFIRMATION
# def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
#     logging.info(f"Processing record ID: {record_id}")

#     try:
#         # Create a VOC bounding box
#         voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
#         logging.debug(f"VOC bounding box created: {voc_bbox}")

#         # Convert VOC bounding box to YOLO format
#         yolo_bbox = voc_bbox.to_yolo()
#         logging.debug(f"YOLO bounding box created: {yolo_bbox}")

#         # Create YOLO label with class_id
#         x_center, y_center, width, height = yolo_bbox.values
#         yolo_label = f"{class_id} {x_center} {y_center} {width} {height}"
#         logging.debug(f"YOLO label created: {yolo_label}")

#         # Create label file path
#         label_file_path = screenshot_path.replace(".png", ".txt").replace(ORIGINAL_SCREENSHOT_DIRECTORY, ORIGINAL_LABELS_DIRECTORY)
#         logging.debug(f"Label file path: {label_file_path}")

#         # Save YOLO label to file
#         with open(label_file_path, "w") as f:
#             f.write(yolo_label)
#         logging.info(f"YOLO label saved to: {label_file_path}")

#         # Load the image
#         image = cv2.imread(resized_image_path)

#         # Convert YOLO values to pixel coordinates
#         x_center_pixel = int(x_center * resized_shape_width)
#         y_center_pixel = int(y_center * resized_shape_height)
#         width_pixel = int(width * resized_shape_width)
#         height_pixel = int(height * resized_shape_height)

#         # Calculate top-left and bottom-right coordinates
#         x1_pixel = x_center_pixel - width_pixel // 2
#         y1_pixel = y_center_pixel - height_pixel // 2
#         x2_pixel = x_center_pixel + width_pixel // 2
#         y2_pixel = y_center_pixel + height_pixel // 2

#         # Draw the bounding box on the image
#         cv2.rectangle(image, (x1_pixel, y1_pixel), (x2_pixel, y2_pixel), (0, 255, 0), 2)

#         # Save the image with the bounding box
#         output_image_path = label_file_path.replace(".txt", "_annotated.png")
#         cv2.imwrite(output_image_path, image)
#         logging.info(f"Annotated image saved to: {output_image_path}")

#     except Exception as e:
#         logging.error(f"Error processing record ID: {record_id} - {str(e)}")




















# # WORKS
# def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
# # def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, screenshot_path):
#     print()
#     print("##### YOLO LABELS #####")
#     # Create a VOC bounding box
#     voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
#     print(f"VOC Bounding Box: {voc_bbox}")
#     print()

#     # Convert VOC bounding box to YOLO format
#     yolo_bbox = voc_bbox.to_yolo()
#     print(f"YOLO Bounding Box: {yolo_bbox}")
#     print()







# def process_and_save_yolo_labels(record_id, class_id, x1, y1, x2, y2, orig_shape_height, orig_shape_width, resized_x1, resized_y1, resized_x2, resized_y2, resized_shape_height, resized_shape_width, screenshot_path, resized_image_path):
#     # Convert original bounding box to YOLO format
#     voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=(orig_shape_width, orig_shape_height))
#     yolo_bbox = voc_bbox.to_yolo()

#     # Debugging: Print type and attributes of original YOLO bounding box
#     print(f"Original YOLO Bounding Box:")
#     print(f"Type of yolo_bbox: {type(yolo_bbox)}")
#     print(f"Attributes of yolo_bbox: {dir(yolo_bbox)}")
#     print(f"Content of yolo_bbox: {yolo_bbox}")

#     # Convert resized bounding box to YOLO format
#     resized_voc_bbox = BoundingBox.from_voc(resized_x1, resized_y1, resized_x2, resized_y2, image_size=(resized_shape_width, resized_shape_height))
#     resized_yolo_bbox = resized_voc_bbox.to_yolo()

#     # Debugging: Print type and attributes of resized YOLO bounding box
#     print(f"Resized YOLO Bounding Box:")
#     print(f"Type of resized_yolo_bbox: {type(resized_yolo_bbox)}")
#     print(f"Attributes of resized_yolo_bbox: {dir(resized_yolo_bbox)}")
#     print(f"Content of resized_yolo_bbox: {resized_yolo_bbox}")

#     # Check if attributes are accessible
#     try:
#         orig_yolo = (yolo_bbox.x_center, yolo_bbox.y_center, yolo_bbox.width, yolo_bbox.height)
#     except AttributeError as e:
#         print(f"Error accessing attributes of yolo_bbox: {e}")
#         orig_yolo = (None, None, None, None)

#     try:
#         resized_yolo = (resized_yolo_bbox.x_center, resized_yolo_bbox.y_center, resized_yolo_bbox.width, resized_yolo_bbox.height)
#     except AttributeError as e:
#         print(f"Error accessing attributes of resized_yolo_bbox: {e}")
#         resized_yolo = (None, None, None, None)

#     # Ensure label directories exist
#     ensure_directory_exists(ORIGINAL_LABELS_DIRECTORY)
#     ensure_directory_exists(RESIZED_LABELS_DIRECTORY)

#     # Save original YOLO label
#     original_yolo_label_path = os.path.join(ORIGINAL_LABELS_DIRECTORY, f"{os.path.splitext(os.path.basename(screenshot_path))[0]}.txt")
#     with open(original_yolo_label_path, 'w') as f:
#         f.write(f"{class_id} {orig_yolo[0]} {orig_yolo[1]} {orig_yolo[2]} {orig_yolo[3]}\n")

#     # Save resized YOLO label
#     resized_yolo_label_path = os.path.join(RESIZED_LABELS_DIRECTORY, f"{os.path.splitext(os.path.basename(screenshot_path))[0]}_resized.txt")
#     with open(resized_yolo_label_path, 'w') as f:
#         f.write(f"{class_id} {resized_yolo[0]} {resized_yolo[1]} {resized_yolo[2]} {resized_yolo[3]}\n")

#     # Update the database with YOLO format data
#     update_database_with_yolo(record_id, orig_yolo, resized_yolo)
#     logging.info(f"YOLO labels and database update successful for record ID {record_id}.")
