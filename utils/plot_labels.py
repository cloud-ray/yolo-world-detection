import cv2
import numpy as np
import os

def plot_scaled_labels(image_path, label_path, output_dir):
    """
    Plot the scaled labels on the resized image.

    Args:
        image_path (str): Path to the resized image file.
        label_path (str): Path to the scaled label file.
        output_dir (str): Directory to save the output image with plotted labels.
    """
    # Load the resized image
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape

    # Load the scaled labels
    with open(label_path, 'r') as file:
        label_lines = file.readlines()

    print(f"Loaded {len(label_lines)} labels from {label_path}")

    # Plot the scaled labels on the image
    for i, line in enumerate(label_lines):
        class_id, x_center, y_center, width, height = map(float, line.strip().split())
        print(f"Label {i+1}: class_id={class_id}, x_center={x_center}, y_center={y_center}, width={width}, height={height}")

        x_center_scaled = int(x_center * image_width)
        y_center_scaled = int(y_center * image_height)
        width_scaled = int(width * image_width)
        height_scaled = int(height * image_height)

        x1 = x_center_scaled - width_scaled // 2
        y1 = y_center_scaled - height_scaled // 2
        x2 = x_center_scaled + width_scaled // 2
        y2 = y_center_scaled + height_scaled // 2

        print(f"  Bounding box coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

        # Draw a rectangle on the image using the bounding box coordinates
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw a point at the center of the bounding box
        cv2.circle(image, (x_center_scaled, y_center_scaled), 5, (0, 0, 255), -1)

    # Save the output image with plotted labels
    output_image_path = os.path.join(output_dir, "labeled_image.jpg")
    cv2.imwrite(output_image_path, image)

    print(f"Output image with plotted labels saved to {output_image_path}")

# Example usage
image_path = "screenshots/resized/images/bird_0_0.66_8.0_1721517879.png"
label_path = "screenshots/resized/labels/bird_0_0.66_8.0_1721517879.txt"
output_dir = "screenshots/resized"

plot_scaled_labels(image_path, label_path, output_dir)