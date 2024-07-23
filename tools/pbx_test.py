from pybboxes import BoundingBox
import json

# test_labeler.py



data = (3, 'deer', 2, 0.458419531583786, 1, 1721661272, 'screenshots/original/screenshots/deer_2_0.46_1.0_1721661272.png', 657.7404174804688, 222.26126098632812, 1109.761474609375, 494.9451599121094, 1080, 1920, 7, 6, './screenshots/resized/without_bbox/deer_2_0.46_1.0_1721661272.jpg', 438.4936116536458, 148.1741739908854, 739.8409830729166, 329.96343994140625, 720, 1280, None, None, None, None, None, None, None, None)

# Extract values
class_id = data[2]
x1 = data[7]
y1 = data[8]
x2 = data[9]
y2 = data[10]
resized_shape = (data[21], data[22])  # (height, width)

from pybboxes import BoundingBox

def convert_bbox_to_yolo(x1, y1, x2, y2, image_size):
    try:
        # Convert VOC bounding box to YOLO format
        voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=image_size)
        print(f"VOC Bounding Box: {voc_bbox}")

        yolo_bbox = voc_bbox.to_yolo()
        print(f"YOLO Bounding Box: {yolo_bbox}")

        return yolo_bbox
    except Exception as e:
        print(f"Error converting bounding box: {e}")

# Example data
example_data = {
    "x1": 657.7404174804688,
    "y1": 222.26126098632812,
    "x2": 1109.761474609375,
    "y2": 494.9451599121094,
    "image_size": (1280, 720)  # (width, height)
}

# Convert example bounding box to YOLO format
yolo_bbox = convert_bbox_to_yolo(
    example_data["x1"],
    example_data["y1"],
    example_data["x2"],
    example_data["y2"],
    example_data["image_size"]
)

print(f"Converted YOLO Bounding Box: {yolo_bbox}")






# import sys
# import os

# # Add the project root directory to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from functions.labeler import process_and_save_yolo_labels

# def test_process_and_save_yolo_labels():
#     # Sample data
#     record_id = 18
#     class_id = 0
#     x1, y1, x2, y2 = 994.7245483398438, 743.4349975585938, 1126.113525390625, 833.4436645507812# VOC coordinates
#     orig_shape = '[1920, 1080]'
#     resized_x1, resized_y1, resized_x2, resized_y2 = 1016.586181640625, 420.05277506510413, 1097.7890625, 519.9231770833333  # Resized VOC coordinates
#     resized_shape = '[1280, 720]'
#     screenshot_path = 'screenshots/original/screenshots/bird_0_0.42_1.0_1721634988.png'

#     # Run the function with the sample data
#     process_and_save_yolo_labels(
#         record_id, class_id, x1, y1, x2, y2, orig_shape,
#         resized_x1, resized_y1, resized_x2, resized_y2, resized_shape,
#         screenshot_path
#     )

# if __name__ == "__main__":
#     test_process_and_save_yolo_labels()










# def convert_bbox_to_yolo(x1, y1, x2, y2, image_size_json):
#     try:
        
#         # Convert VOC bounding box to YOLO format
#         voc_bbox = BoundingBox.from_voc(x1, y1, x2, y2, image_size=image_size)
#         print(f"VOC Bounding Box: {voc_bbox}")

#         yolo_bbox = voc_bbox.to_yolo()
#         print(f"YOLO Bounding Box: {yolo_bbox}")

#         return yolo_bbox

#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")

# # Example data from your resized values
# example_data = {
#     "x1": 1016.2478841145833,
#     "y1": 419.6207275390625,
#     "x2": 1098.072998046875,
#     "y2": 519.9530843098958,
#     "resized_shape": "[1280, 720]"
# }

# # Convert example bounding box to YOLO format
# convert_bbox_to_yolo(example_data["x1"], example_data["y1"], example_data["x2"], example_data["y2"], example_data["resized_shape"])


# import cv2
# import matplotlib.pyplot as plt

# # Load the image
# image_path = './screenshots/resized/without_bbox/bird_0_0.45_2.0_1721631027.jpg'
# image = cv2.imread(image_path)

# if image is None:
#     print("Failed to read the image. Check the image path and file.")
# else:
#     # Define the image size
#     image_size = (1280, 720)  # Add the image size as a variable

#     # Define the bounding box coordinates in YOLO format
#     yolo_bbox = [0.8258, 0.6528, 0.0641, 0.1389]

#     # Convert YOLO coordinates to pixel coordinates
#     image_width, image_height = image_size
#     x_center = int(yolo_bbox[0] * image_width)
#     y_center = int(yolo_bbox[1] * image_height)
#     width = int(yolo_bbox[2] * image_width)
#     height = int(yolo_bbox[3] * image_height)

#     # Calculate the top-left and bottom-right coordinates of the bounding box
#     x1 = x_center - width // 2
#     y1 = y_center - height // 2
#     x2 = x_center + width // 2
#     y2 = y_center + height // 2

#     # Draw the bounding box on the image
#     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

#     # Display the image with the bounding box
#     plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     plt.show()