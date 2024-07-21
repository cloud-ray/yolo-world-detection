def scale_bounding_box(bbox, scale_x, scale_y):
    """Scale bounding box coordinates."""
    return (
        int(bbox['x1'] * scale_x), int(bbox['y1'] * scale_y),
        int(bbox['x2'] * scale_x), int(bbox['y2'] * scale_y)
    )

def print_bounding_box_details(orig_bbox, new_bbox, orig_shape, new_size, scale_x, scale_y):
    """Print original and new bounding box details."""
    orig_x1, orig_y1, orig_x2, orig_y2 = orig_bbox
    new_x1, new_y1, new_x2, new_y2 = new_bbox

    print(f"Original image size: {orig_shape[1]}x{orig_shape[0]}")
    print(f"Original bounding box: ({orig_x1}, {orig_y1}), ({orig_x2}, {orig_y2})")
    print(f"New image size: {new_size[1]}x{new_size[0]}")
    print(f"New bounding box: ({new_x1}, {new_y1}), ({new_x2}, {new_y2})")
    print(f"Width scaling factor: {scale_x}")
    print(f"Height scaling factor: {scale_y}")
