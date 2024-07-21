import json
import os
from utils.bbox_utils import scale_bounding_box

def load_json_data(json_path):
    """Load JSON data from a file."""
    with open(json_path, 'r') as file:
        return json.load(file)

def ensure_output_folder_exists(output_folder):
    """Ensure the output folder exists."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def save_scaled_bboxes_to_json(json_path, new_size, data):
    """Save scaled bounding boxes to a JSON file."""
    new_data = {"objects": []}

    for obj in data['objects']:
        image_path = obj['image_path']
        bbox = obj['bbox']
        orig_shape = obj['orig_shape']
        orig_height, orig_width = orig_shape

        scale_x = new_size[1] / orig_width
        scale_y = new_size[0] / orig_height

        new_bbox = scale_bounding_box(bbox, scale_x, scale_y)

        new_data_obj = {
            "image_path": image_path,
            "bbox": {
                "x1": new_bbox[0],
                "y1": new_bbox[1],
                "x2": new_bbox[2],
                "y2": new_bbox[3]
            },
            "orig_shape": orig_shape
        }

        new_data["objects"].append(new_data_obj)

    # Ensure the directory for the JSON file exists
    json_dir = os.path.dirname(json_path)
    ensure_output_folder_exists(json_dir)

    with open(json_path, 'w') as json_file:
        json.dump(new_data, json_file, indent=4)

    print(f"Saved scaled bounding boxes to {json_path}")
