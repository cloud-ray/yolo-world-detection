# utils/image_utils.py
import cv2

def resize_image(image, new_size):
    """Resize an image to a new size."""
    return cv2.resize(image, new_size)

def draw_bounding_box(image, bbox, color=(0, 255, 0), thickness=2):
    """Draw a bounding box on an image."""
    x1, y1, x2, y2 = bbox
    return cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

def save_resized_image(image, output_path, quality=90):
    """Save the resized image with the specified quality."""
    cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
