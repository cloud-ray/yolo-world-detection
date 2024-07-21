# functions/screenshot_resizer.py
import os
import sys
import cv2

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.image_utils import resize_image, draw_bounding_box, save_resized_image
from utils.bbox_utils import scale_bounding_box, print_bounding_box_details
from utils.file_utils import load_json_data, ensure_output_folder_exists, save_scaled_bboxes_to_json

# Constants
NEW_IMAGE_SIZE = (720, 1280)  # Adjust as needed
IMAGE_QUALITY = 90
PRINT_WITH_COORDS = True
RESIZED_IMAGE_DIRECTORY = "screenshots/resized/without_bbox"
RESIZED_IMAGE_BBOX_DIRECTORY = "screenshots/resized/with_bbox"
JSON_IMAGE_DATA_FILE = "screenshots/json/screenshot_data.json"
JSON_RESIZED_DIRECTORY = "screenshots/resized/json"
JSON_RESIZED_FILE_NAME = "resized_bbox_data.json"

def resize_image_and_bboxes(json_path, output_folder_with_bbox, output_folder_without_bbox, new_size=NEW_IMAGE_SIZE, print_with_coords=PRINT_WITH_COORDS):
    """Resize images and bounding boxes according to new size, with options to save with and without bounding boxes."""
    data = load_json_data(json_path)
    ensure_output_folder_exists(output_folder_with_bbox)
    ensure_output_folder_exists(output_folder_without_bbox)

    new_height, new_width = new_size

    for obj in data['objects']:
        image_path = obj['image_path']
        bbox = obj['bbox']
        orig_shape = obj['orig_shape']
        orig_height, orig_width = orig_shape

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to open image {image_path}")
            continue

        scale_x = new_width / orig_width
        scale_y = new_height / orig_height

        resized_image = resize_image(image, (new_width, new_height))
        new_bbox = scale_bounding_box(bbox, scale_x, scale_y)

        if print_with_coords:
            orig_bbox = (bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2'])
            print_bounding_box_details(orig_bbox, new_bbox, orig_shape, new_size, scale_x, scale_y)
            image_with_bbox = draw_bounding_box(resized_image.copy(), new_bbox)

            filename_with_bbox = os.path.basename(image_path).replace('.png', '.jpg')
            output_path_with_bbox = os.path.join(output_folder_with_bbox, filename_with_bbox)

            save_resized_image(image_with_bbox, output_path_with_bbox, quality=IMAGE_QUALITY)
            print(f"Saved resized image WITH bounding box to {output_path_with_bbox}")
        else:
            filename_without_bbox = os.path.basename(image_path).replace('.png', '.jpg')
            output_path_without_bbox = os.path.join(output_folder_without_bbox, filename_without_bbox)

            save_resized_image(resized_image, output_path_without_bbox, quality=IMAGE_QUALITY)
            print(f"Saved resized image WITHOUT bounding box to {output_path_without_bbox}")

        # Save scaled bounding boxes to a JSON file
        scaled_json_path = os.path.join(JSON_RESIZED_DIRECTORY, JSON_RESIZED_FILE_NAME)
        save_scaled_bboxes_to_json(scaled_json_path, new_size, data)

# Example usage
resize_image_and_bboxes(
    JSON_IMAGE_DATA_FILE,
    RESIZED_IMAGE_BBOX_DIRECTORY,
    RESIZED_IMAGE_DIRECTORY,
    new_size=NEW_IMAGE_SIZE,
    print_with_coords=PRINT_WITH_COORDS
)







# # FUNCTIONS AS MONOLITH
# import json
# import cv2
# import os

# # Current orig_shape | Standard Aspect Ratio (9:16) | 1080 x 1920
# NEW_IMAGE_SIZE = (720, 1280) # (67% of original size)
# # NEW_IMAGE_SIZE = (540, 960) # (50% of original size)
# # NEW_IMAGE_SIZE = (360, 640) # (33% of original size)

# IMAGE_QUALITY = 90  # adjust this value to change the image quality

# # PRINT_WITH_COORDS (bool): If True, prints details of bounding boxes and scaling. 
# # If False, only resizes images and bounding boxes without printing details.
# PRINT_WITH_COORDS = True 

# RESIZED_IMAGE_DIRECTORY = "screenshots/resized/without_bbox"

# RESIZED_IMAGE_BBOX_DIRECTORY = "screenshots/resized/with_bbox"

# JSON_IMAGE_DATA_FILE = "screenshots/json/screenshot_data.json"

# JSON_RESIZED_DIRECTORY = "screenshots/resized/json"

# JSON_RESIZED_FILE_NAME = "resized_bbox_data.json"

# def load_json_data(json_path):
#     """Load JSON data from a file."""
#     with open(json_path, 'r') as file:
#         return json.load(file)

# def ensure_output_folder_exists(output_folder):
#     """Ensure the output folder exists."""
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

# def resize_image(image, new_size):
#     """Resize an image to a new size."""
#     return cv2.resize(image, new_size)

# def scale_bounding_box(bbox, scale_x, scale_y):
#     """Scale bounding box coordinates."""
#     return (
#         int(bbox['x1'] * scale_x), int(bbox['y1'] * scale_y),
#         int(bbox['x2'] * scale_x), int(bbox['y2'] * scale_y)
#     )

# def draw_bounding_box(image, bbox, color=(0, 255, 0), thickness=2):
#     """Draw a bounding box on an image."""
#     x1, y1, x2, y2 = bbox
#     return cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

# def save_resized_image(image, output_path, quality=IMAGE_QUALITY):
#     """Save the resized image with the specified quality."""
#     cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])

# def print_bounding_box_details(orig_bbox, new_bbox, orig_shape, new_size, scale_x, scale_y):
#     """Print original and new bounding box details."""
#     orig_x1, orig_y1, orig_x2, orig_y2 = orig_bbox
#     new_x1, new_y1, new_x2, new_y2 = new_bbox

#     print(f"Original image size: {orig_shape[1]}x{orig_shape[0]}")
#     print(f"Original bounding box: ({orig_x1}, {orig_y1}), ({orig_x2}, {orig_y2})")
#     print(f"New image size: {new_size[1]}x{new_size[0]}")
#     print(f"New bounding box: ({new_x1}, {new_y1}), ({new_x2}, {new_y2})")
#     print(f"Width scaling factor: {scale_x}")
#     print(f"Height scaling factor: {scale_y}")

# def resize_image_and_bboxes(json_path, output_folder_with_bbox, output_folder_without_bbox, new_size=NEW_IMAGE_SIZE, print_with_coords=PRINT_WITH_COORDS):
#     """Resize images and bounding boxes according to new size, with options to save with and without bounding boxes."""
#     data = load_json_data(json_path)
#     ensure_output_folder_exists(output_folder_with_bbox)
#     ensure_output_folder_exists(output_folder_without_bbox)

#     new_height, new_width = new_size

#     for obj in data['objects']:
#         image_path = obj['image_path']
#         bbox = obj['bbox']
#         orig_shape = obj['orig_shape']
#         orig_height, orig_width = orig_shape

#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"Error: Unable to open image {image_path}")
#             continue

#         scale_x = new_width / orig_width
#         scale_y = new_height / orig_height

#         resized_image = resize_image(image, (new_width, new_height))
#         new_bbox = scale_bounding_box(bbox, scale_x, scale_y)

#         if print_with_coords:
#             orig_bbox = (bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2'])
#             print_bounding_box_details(orig_bbox, new_bbox, orig_shape, new_size, scale_x, scale_y)
#             image_with_bbox = draw_bounding_box(resized_image.copy(), new_bbox)

#             filename_with_bbox = os.path.basename(image_path).replace('.png', '.jpg')
#             output_path_with_bbox = os.path.join(output_folder_with_bbox, filename_with_bbox)

#             save_resized_image(image_with_bbox, output_path_with_bbox)
#             print(f"Saved resized image WITH bounding box to {output_path_with_bbox}")
#         else:
#             filename_without_bbox = os.path.basename(image_path).replace('.png', '.jpg')
#             output_path_without_bbox = os.path.join(output_folder_without_bbox, filename_without_bbox)

#             save_resized_image(resized_image, output_path_without_bbox)
#             print(f"Saved resized image WITHOUT bounding box to {output_path_without_bbox}")

#         # Save scaled bounding boxes to a JSON file
#         scaled_json_path = os.path.join(JSON_RESIZED_DIRECTORY, JSON_RESIZED_FILE_NAME)
#         save_scaled_bboxes_to_json(scaled_json_path, new_size, data)

# # Example usage
# resize_image_and_bboxes(
#     JSON_IMAGE_DATA_FILE,
#     RESIZED_IMAGE_BBOX_DIRECTORY,
#     RESIZED_IMAGE_DIRECTORY,
#     new_size=NEW_IMAGE_SIZE,
#     print_with_coords=PRINT_WITH_COORDS
# )

# def save_scaled_bboxes_to_json(json_path, new_size, data):
#     """Save scaled bounding boxes to a JSON file."""
#     new_data = {"objects": []}

#     for obj in data['objects']:
#         image_path = obj['image_path']
#         bbox = obj['bbox']
#         orig_shape = obj['orig_shape']
#         orig_height, orig_width = orig_shape

#         scale_x = new_size[1] / orig_width
#         scale_y = new_size[0] / orig_height

#         new_bbox = scale_bounding_box(bbox, scale_x, scale_y)

#         new_data_obj = {
#             "image_path": image_path,
#             "bbox": {
#                 "x1": new_bbox[0],
#                 "y1": new_bbox[1],
#                 "x2": new_bbox[2],
#                 "y2": new_bbox[3]
#             },
#             "orig_shape": orig_shape
#         }

#         new_data["objects"].append(new_data_obj)

#     with open(json_path, 'w') as json_file:
#         json.dump(new_data, json_file, indent=4)

#     print(f"Saved scaled bounding boxes to {json_path}")












# # WORKS BEFORE MODULARIZING
# def resize_image_and_bboxes(json_path, output_folder, new_size=(720, 1280), PRINT_WITH_COORDS=True):
#     # Load the JSON file
#     with open(json_path, 'r') as file:
#         data = json.load(file)
    
#     # Ensure the output folder exists
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     # Get new dimensions
#     new_height, new_width = new_size
    
#     # Iterate through each object in the JSON data
#     for obj in data['objects']:
#         image_path = obj['image_path']
#         bbox = obj['bbox']
#         orig_shape = obj['orig_shape']
#         orig_height, orig_width = orig_shape
        
#         # Read the image
#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"Error: Unable to open image {image_path}")
#             continue
        
#         # Calculate the scaling factors
#         scale_x = new_width / orig_width
#         scale_y = new_height / orig_height
        
#         # Resize the image
#         resized_image = cv2.resize(image, (new_width, new_height))
        
#         # Resize the bounding box coordinates
#         x1, y1, x2, y2 = (int(bbox['x1'] * scale_x), int(bbox['y1'] * scale_y),
#                            int(bbox['x2'] * scale_x), int(bbox['y2'] * scale_y))
        
#         # Print original and new bounding box details
#         orig_x1, orig_y1, orig_x2, orig_y2 = int(bbox['x1']), int(bbox['y1']), int(bbox['x2']), int(bbox['y2'])
#         print(f"Original image size: {orig_width}x{orig_height}")
#         print(f"Original bounding box: ({orig_x1}, {orig_y1}), ({orig_x2}, {orig_y2})")
#         print(f"New image size: {new_width}x{new_height}")
#         print(f"New bounding box: ({x1}, {y1}), ({x2}, {y2})")
        
#         # Check if the scaling is consistent
#         orig_width_bbox = orig_x2 - orig_x1
#         orig_height_bbox = orig_y2 - orig_y1
#         new_width_bbox = x2 - x1
#         new_height_bbox = y2 - y1
        
#         print(f"Original bounding box width: {orig_width_bbox}")
#         print(f"Original bounding box height: {orig_height_bbox}")
#         print(f"New bounding box width: {new_width_bbox}")
#         print(f"New bounding box height: {new_height_bbox}")
#         print(f"Width scaling factor: {scale_x}")
#         print(f"Height scaling factor: {scale_y}")
        
#         if PRINT_WITH_COORDS:
#             # Draw the bounding box
#             color = (0, 255, 0)  # Green color for the bounding box
#             thickness = 2
#             resized_image = cv2.rectangle(resized_image, (x1, y1), (x2, y2), color, thickness)
        
#         # Convert the image to JPEG format with quality 90
#         filename = os.path.basename(image_path).replace('.png', '.jpg')
#         output_path = os.path.join(output_folder, filename)
        
#         # Save the resized image with bounding box as JPEG
#         cv2.imwrite(output_path, resized_image, [cv2.IMWRITE_JPEG_QUALITY, IMAGE_QUALITY])
#         print(f"Saved resized image with bounding box to {output_path}")

# # Example usage
# resize_image_and_bboxes(JSON_IMAGE_DATA_FILE, RESIZED_IMAGE_DIRECTORY, PRINT_WITH_COORDS=PRINT_WITH_COORDS)













# VIEW AND COMPARE IMAGE SIZES
# def compare_image_sizes(orig_folder_path, resized_folder_path):
#     for filename in os.listdir(orig_folder_path):
#         if filename.endswith('.png'):
#             base_filename = filename[:-4]  # remove the .png extension
#             jpg_filename = base_filename + '.jpg'
#             if jpg_filename in os.listdir(resized_folder_path):
#                 orig_file_path = os.path.join(orig_folder_path, filename)
#                 resized_file_path = os.path.join(resized_folder_path, jpg_filename)

#                 orig_file_size_bytes = os.path.getsize(orig_file_path)
#                 resized_file_size_bytes = os.path.getsize(resized_file_path)

#                 orig_file_size_mb = orig_file_size_bytes / (1024 * 1024)
#                 orig_file_size_kb = orig_file_size_bytes / 1024

#                 resized_file_size_mb = resized_file_size_bytes / (1024 * 1024)
#                 resized_file_size_kb = resized_file_size_bytes / 1024

#                 data_saved_mb = orig_file_size_mb - resized_file_size_mb
#                 data_saved_kb = orig_file_size_kb - resized_file_size_kb

#                 print(f"{base_filename}:")
#                 print(f"  Original: {orig_file_size_mb:.2f} MB ({orig_file_size_kb:.2f} KB)")
#                 print(f"  Resized: {resized_file_size_mb:.2f} MB ({resized_file_size_kb:.2f} KB)")
#                 print(f"  Data saved: {data_saved_mb:.2f} MB ({data_saved_kb:.2f} KB)")
#                 print()

# # Call the function with the folder paths
# compare_image_sizes("screenshots/images", "screenshots/resized/images")