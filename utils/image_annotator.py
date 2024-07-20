import os
import cv2

# Directory paths
IMAGE_DIRECTORY = "./screenshots/images"
LABEL_DIRECTORY = "./screenshots/labels"
ANNOTATE_DIRECTORY = "./screenshots/annotated"

# Ensure the annotated directory exists
os.makedirs(ANNOTATE_DIRECTORY, exist_ok=True)

def read_labels(label_file):
    """
    Reads bounding box labels from a text file.
    Args:
        label_file (str): Path to the label file.
    Returns:
        list: A list of bounding boxes with format (class_idx, center_x, center_y, box_width, box_height).
    """
    with open(label_file, 'r') as file:
        lines = file.readlines()
        boxes = [list(map(float, line.strip().split())) for line in lines]
    return boxes

def extract_info_from_filename(filename):
    """
    Extracts class name, class ID, confidence, and track ID from the filename.
    Args:
        filename (str): The filename of the image.
    Returns:
        tuple: (class_name, class_id, confidence, track_id)
    """
    base_name = os.path.splitext(filename)[0]
    parts = base_name.split('_')
    class_name = parts[0]
    class_id = int(parts[1])
    confidence = float(parts[2])
    track_id = int(float(parts[3]))  # Convert track ID to int
    return class_name, class_id, confidence, track_id

def draw_bounding_boxes(image, boxes, class_name, class_id, confidence, track_id):
    """
    Draws bounding boxes on the image and annotates with class name, ID, confidence, and track ID.
    Args:
        image (numpy.ndarray): The image on which to draw.
        boxes (list): A list of bounding boxes with format (class_idx, center_x, center_y, box_width, box_height).
        class_name (str): The class name for the objects.
        class_id (int): The class ID for the objects.
        confidence (float): The confidence score for the objects.
        track_id (int): The tracking ID for the objects.
    Returns:
        numpy.ndarray: The image with drawn bounding boxes and annotations.
    """
    height, width, _ = image.shape
    font_scale = 0.8  # Increase to make text larger
    font_thickness = 2  # Increase to make text bolder

    for box in boxes:
        class_idx, center_x, center_y, box_width, box_height = box
        # Convert from relative to absolute coordinates
        top_left_x = int((center_x - box_width / 2) * width)
        top_left_y = int((center_y - box_height / 2) * height)
        bottom_right_x = int((center_x + box_width / 2) * width)
        bottom_right_y = int((center_y + box_height / 2) * height)
        # Draw rectangle
        cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)
        # Annotate class name, class ID, confidence, and track ID
        label = f"{class_name} Class_ID: {class_id} Conf: {confidence:.2f} Track_ID: {track_id}"
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        text_width, text_height = text_size
        # Draw background rectangle for text
        cv2.rectangle(image, (top_left_x, top_left_y - text_height - 10), (top_left_x + text_width, top_left_y), (255, 255, 255), -1)
        # Draw the text
        cv2.putText(image, label, (top_left_x, top_left_y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)
    return image

def process_images(image_directory, label_directory, annotate_directory):
    """
    Processes images by reading their corresponding labels and drawing bounding boxes.
    Args:
        image_directory (str): Path to the directory containing images.
        label_directory (str): Path to the directory containing label files.
        annotate_directory (str): Path to the directory to save annotated images.
    """
    for image_name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, image_name)
        label_path = os.path.join(label_directory, image_name.replace('.png', '.txt'))

        if os.path.exists(label_path):
            image = cv2.imread(image_path)
            boxes = read_labels(label_path)
            class_name, class_id, confidence, track_id = extract_info_from_filename(image_name)
            annotated_image = draw_bounding_boxes(image, boxes, class_name, class_id, confidence, track_id)
            annotated_image_path = os.path.join(annotate_directory, image_name)
            cv2.imwrite(annotated_image_path, annotated_image)
            print(f"Annotated image saved at {annotated_image_path}")

if __name__ == "__main__":
    process_images(IMAGE_DIRECTORY, LABEL_DIRECTORY, ANNOTATE_DIRECTORY)
