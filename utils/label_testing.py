import cv2
import numpy as np
import os

def resize_image_and_scale_labels(image_path, label_path, new_width, new_height, quality, output_dir):
    """
    Resize the image and scale the labels accordingly.

    Args:
        image_path (str): Path to the image file.
        label_path (str): Path to the label file.
        new_width (int): New width of the image.
        new_height (int): New height of the image.
        quality (int): Quality of the resized image (0-100).
        output_dir (str): Directory to save the resized image and scaled labels.
    """
    # Load the image
    image = cv2.imread(image_path)

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    # Save the resized image with the specified quality
    image_filename = os.path.basename(image_path)
    resized_image_path = os.path.join(output_dir, "images", image_filename)
    cv2.imwrite(resized_image_path, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])

    # Load the label file
    with open(label_path, 'r') as file:
        label_lines = file.readlines()

    # Print original labels
    print("Original labels:")
    for line in label_lines:
        print(line.strip())

    # Scale the labels
    scaled_labels = []
    for line in label_lines:
        class_id, x_center, y_center, width, height = map(float, line.strip().split())
        x_center_scaled = x_center * new_width / image.shape[1]
        y_center_scaled = y_center * new_height / image.shape[0]
        width_scaled = width * new_width / image.shape[1]
        height_scaled = height * new_height / image.shape[0]
        scaled_labels.append(f"{class_id} {x_center_scaled} {y_center_scaled} {width_scaled} {height_scaled}")

    # Print scaled labels
    print("\nScaled labels:")
    for line in scaled_labels:
        print(line)

    # Save the scaled labels
    label_filename = os.path.basename(label_path)
    scaled_label_path = os.path.join(output_dir, "labels", label_filename)
    with open(scaled_label_path, 'w') as file:
        file.write('\n'.join(scaled_labels))

    # Confirmation
    print("\nConfirmation:")
    for i, (original, scaled) in enumerate(zip(label_lines, scaled_labels)):
        original_class_id, original_x_center, original_y_center, original_width, original_height = map(float, original.strip().split())
        scaled_class_id, scaled_x_center, scaled_y_center, scaled_width, scaled_height = map(float, scaled.split())
        print(f"Object {i+1}:")
        print(f"  Original: x_center={original_x_center:.4f}, y_center={original_y_center:.4f}, width={original_width:.4f}, height={original_height:.4f}")
        print(f"  Scaled:   x_center={scaled_x_center:.4f}, y_center={scaled_y_center:.4f}, width={scaled_width:.4f}, height={scaled_height:.4f}")
        print(f"  Scaling factor: x={new_width/image.shape[1]:.4f}, y={new_height/image.shape[0]:.4f}")
        print()

# Example usage
image_path = "screenshots/images/bird_0_0.66_8.0_1721517879.png"
label_path = "screenshots/labels/bird_0_0.66_8.0_1721517879.txt"
new_width = 1280
new_height = 720
quality = 90
output_dir = "screenshots/resized"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(os.path.join(output_dir, "images")):
    os.makedirs(os.path.join(output_dir, "images"))
if not os.path.exists(os.path.join(output_dir, "labels")):
    os.makedirs(os.path.join(output_dir, "labels"))

resize_image_and_scale_labels(image_path, label_path, new_width, new_height, quality, output_dir)