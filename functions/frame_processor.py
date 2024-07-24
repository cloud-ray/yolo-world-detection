# functions/frame_processor.py

# Standard library imports
import time

# Third-party library imports
import cv2
import logging

# Project-specific imports
from functions.object_tracker import update_object_tracker
from functions.screenshot_handler import check_and_save_screenshot

# Utility imports
from utils.logger import setup_logging
from utils.frame_utils import FPSCounter

# Configuration imports
from utils.config import (
    MODEL_TRACK_CONF,
    MODEL_TRACK_IOU,
    TRACKER_CONFIG_PATH,
    DETECTION_INTERVAL
)

# Set up logging
setup_logging()

# Initialize FPS counter
fps_counter = FPSCounter()

# Initialize detection timer
last_detection_time = time.time()

# Flag to control the display of bounding boxes on detected objects.
# Set SHOW_BOUNDING_BOX to True to display bounding boxes on screenshots during testing.
# This is useful for debugging and verifying detection accuracy.
# Set SHOW_BOUNDING_BOX to False to capture screenshots without bounding boxes for use as training data.
SHOW_BOUNDING_BOX = True


def process_frame(model, classes, frame):
    """
    Process a video frame to detect and track objects.

    Args:
        model: The object detection and tracking model.
        classes: List of class names for detected objects.
        frame: The video frame to process.

    Returns:
        Processed video frame with optional bounding box annotations.
    """
    global fps_counter, last_detection_time

    # Calculate FPS
    fps = fps_counter.update()
    if fps:
        logging.info(f"FPS: {fps:.2f}")

    # Check if the detection interval has passed
    current_time = time.time()
    if current_time - last_detection_time >= DETECTION_INTERVAL:
        last_detection_time = current_time
        try:
            # Track objects in the frame using the tracker configuration from the config file
            results = model.track(
                source=frame, 
                persist=True, 
                tracker=TRACKER_CONFIG_PATH,
                conf=MODEL_TRACK_CONF, 
                iou=MODEL_TRACK_IOU, 
                classes=None, 
                verbose=True 
            )

            last_detection_time = current_time

            if not results:
                logging.info("No objects detected in the frame.")
                return frame

            # Log the speed of the results
            log_speed(results[0].speed)

            for result in results:
                boxes = result.boxes
                if not boxes:
                    logging.debug("No bounding boxes found in the results.")
                    continue

                xyxy, conf, cls, ids, orig_shape = extract_box_details(boxes)

                for i in range(len(xyxy)):
                    x1, y1, x2, y2 = xyxy[i]
                    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
                    confidence = conf[i]
                    class_idx = int(cls[i])
                    obj_id = ids[i]

                    # Update object state and check conditions
                    if obj_id is not None:
                        update_object_tracker(obj_id, confidence)

                        print_detected_item(classes, class_idx, confidence, x1, y1, x2, y2, obj_id)

                        check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, x1, y1, x2, y2, orig_shape)

                    # Draw bounding boxes, labels, and IDs on the frame if enabled
                    if SHOW_BOUNDING_BOX:
                        draw_boxes_and_labels(frame, classes, class_idx, confidence, x1, y1, x2, y2, obj_id)

        except Exception as e:
            logging.error(f"Error processing frame: {e}")

    return frame

def log_speed(speed):
    """
    Log the speed of various processing stages for the frame.

    Args:
        speed (dict): Dictionary containing the processing speed for 'preprocess',
                      'inference', and 'postprocess' stages.
    """
    try:
        logging.debug(f"Speed: {speed['preprocess']:.3f}ms preprocess, {speed['inference']:.3f}ms inference, {speed['postprocess']:.3f}ms postprocess per image")
    except KeyError as e:
        logging.error(f"Speed data missing key: {e}")

def extract_box_details(boxes):
    """
    Extract bounding box details from detected objects.

    Args:
        boxes: The bounding box data from the detection results.

    Returns:
        A tuple containing lists of bounding box coordinates, confidence scores, 
        class indices, object IDs, and original image shape.
    """
    try:
        xyxy = boxes.xyxy.detach().tolist()
        conf = boxes.conf.detach().tolist()
        cls = boxes.cls.detach().tolist()
        ids = boxes.id.detach().tolist() if hasattr(boxes, 'id') and boxes.id is not None else [None] * len(xyxy)
        orig_shape = (boxes.orig_shape[1], boxes.orig_shape[0])  # Swap width and height

        return xyxy, conf, cls, ids, orig_shape
    except AttributeError as e:
        logging.error(f"Error extracting box details: {e}")
        return [], [], [], [], (0, 0)


def print_detected_item(classes, class_idx, confidence, x1, y1, x2, y2, obj_id):
    """
    Log information about detected items.

    Args:
        classes (list): List of class names.
        class_idx (int): Index of the detected class.
        confidence (float): Confidence score of the detection.
        x1, y1, x2, y2 (float): Bounding box coordinates.
        obj_id: ID of the detected object.
    """
    logging.info(f"Detected item: {classes[class_idx]} with confidence {confidence:.2f} at coordinates ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}), ID: {obj_id}")

def draw_boxes_and_labels(frame, classes, class_idx, confidence, x1, y1, x2, y2, obj_id):
    """
    Draw bounding boxes and labels on the frame.

    Args:
        frame: The video frame to draw on.
        classes (list): List of class names.
        class_idx (int): Index of the detected class.
        confidence (float): Confidence score of the detection.
        x1, y1, x2, y2 (int): Bounding box coordinates.
        obj_id: ID of the detected object.

    Draws bounding boxes and labels on the frame for detected objects, including
    class name, confidence score, and object ID.
    """
    try:
        # Convert coordinates to integers for drawing
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Debug logging for coordinate values and types
        # logging.debug(f"Drawing rectangle with coordinates: ({x1}, {y1}), ({x2}, {y2})")

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw class label and confidence
        label = f"{classes[class_idx]} {confidence:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if obj_id is not None:
            id_label = f"ID: {int(obj_id)}"
            cv2.putText(frame, id_label, (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            logging.warning("obj_id is None or invalid")
    except Exception as e:
        logging.error(f"Error drawing bounding box and labels: {e}")
