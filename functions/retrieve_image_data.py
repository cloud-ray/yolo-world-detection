import os
from PIL import Image

def retrieve_image_data(image_path):
  """
  Retrieves image data from the specified path, prints shape and bounding box coordinates.

  Args:
      image_path (str): Path to the image file.

  Returns:
      None
  """
  if not os.path.exists(image_path):
    print(f"Image not found: {image_path}")
    return

  try:
    # Open image using Pillow (PIL Fork)
    image = Image.open(image_path)

    # Get image shape (width, height)
    image_shape = image.size

    # Extract bounding box coordinates from filename (assuming the format used in screenshot_handler.py)
    filename = os.path.basename(image_path)
    _, class_id, confidence, obj_id, x1, y1, x2, y2, _ = filename.split("_")

    # Try converting coordinates to integers, handle non-integers gracefully
    try:
      x1 = int(x1)
      y1 = int(y1)
    except ValueError:
      # If conversion fails, use the original string values (might be floats)
      print(f"Warning: Unable to convert coordinates to integers for {image_path}")
      pass
    x2 = int(x2)
    y2 = int(y2)

    # Print image information
    print(f"Image Path: {image_path}")
    print(f"Image Shape: {image_shape}")
    print(f"Bounding Box: (x1, y1), (x2, y2) = ({x1}, {y1}), ({x2}, {y2})")

  except Exception as e:
    print(f"Error retrieving image data: {e}")

# Example usage with the problematic file
retrieve_image_data(image_path="screenshots/images/deer_2_0.62_1.0_915.2326049804688_611.9567260742188_1155.6446533203125_852.187255859375_1721543757.png")
