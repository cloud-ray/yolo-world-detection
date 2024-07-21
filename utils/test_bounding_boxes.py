# utils/test_bounding_boxes.py
import json
import cv2
import os

def plot_bounding_boxes(json_path, output_folder):
    # Load the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through each object in the JSON data
    for obj in data['objects']:
        image_path = obj['image_path']
        bbox = obj['bbox']
        orig_shape = obj['orig_shape']
        print(orig_shape)
        
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to open image {image_path}")
            continue
        
        # Draw the bounding box
        x1, y1, x2, y2 = int(bbox['x1']), int(bbox['y1']), int(bbox['x2']), int(bbox['y2'])
        color = (0, 255, 0)  # Green color for the bounding box
        thickness = 2
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        
        # Save the image with bounding box
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, image)
        print(f"Saved annotated image to {output_path}")

# Example usage
plot_bounding_boxes('screenshots/json/screenshot_data.json', 'screenshots/json')
