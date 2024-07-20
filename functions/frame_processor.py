# functions/frame_processor.py
import cv2
import time
import logging
from utils.config import MODEL_TRACK_CONF, MODEL_TRACK_IOU, TRACKER_CONFIG_PATH, DETECTION_INTERVAL
from functions.object_tracker import update_object_tracker
from functions.screenshot_handler import check_and_save_screenshot
from utils.logger import setup_logging
from utils.frame_utils import FPSCounter, throttle_frame_rate

# Set up logging
setup_logging()

# Initialize FPS counter
fps_counter = FPSCounter()

# Initialize detection timer
last_detection_time = time.time()

# Flag to determine whether to save annotated images or clean images
SAVE_ANNOTATED_IMAGES = True

def process_frame(model, classes, frame):
    """
    Process a video frame, perform object tracking, and handle detected objects.

    Args:   
        model (object): The object detection/tracking model.
        classes (list): List of class names.
        frame (numpy.ndarray): The image frame to process.

    Returns:
        numpy.ndarray: The processed frame with or without drawn bounding boxes and labels.
    """
    global fps_counter, last_detection_time

    # Calculate FPS
    fps = fps_counter.update()
    if fps:
        logging.info(f"FPS: {fps:.2f}")

    # Throttle frame rate to control display speed
    if fps:  # Ensure fps is not None before passing it
        frame, process_frame_flag = throttle_frame_rate(frame, fps)
        if not process_frame_flag:
            logging.debug("Frame skipped due to throttling.")
            return frame

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

            height, width, _ = frame.shape

            # Log the speed of the results
            log_speed(results[0].speed)

            for result in results:
                boxes = result.boxes
                if not boxes:
                    logging.info("No bounding boxes found in the results.")
                    continue

                xyxy, conf, cls, ids = extract_box_details(boxes)

                for i in range(len(xyxy)):
                    x1, y1, x2, y2 = xyxy[i]
                    confidence = conf[i]
                    class_idx = int(cls[i])
                    obj_id = ids[i]

                    # Update object state and check conditions
                    if obj_id is not None:
                        update_object_tracker(obj_id, confidence)
                        
                        center_x, center_y, box_width, box_height = convert_to_yolo_format(x1, y1, x2, y2, width, height)
                        
                        # Save screenshot and label file
                        check_and_save_screenshot(obj_id, class_idx, confidence, frame, classes, center_x, center_y, box_width, box_height)

                    # Draw bounding boxes, labels, and IDs on the frame if enabled
                    if SAVE_ANNOTATED_IMAGES:
                        print_detected_item(classes, class_idx, confidence, x1, y1, x2, y2, obj_id)
                        draw_boxes_and_labels(frame, classes, class_idx, confidence, x1, y1, x2, y2, obj_id)

        except Exception as e:
            logging.error(f"Error processing frame: {e}")

    return frame

def log_speed(speed):
    """
    Log the speed of the model's operations.

    Args:
        speed (dict): Dictionary containing speed metrics for preprocessing, inference, and postprocessing.
    """
    logging.debug(f"Speed: {speed['preprocess']:.3f}ms preprocess, {speed['inference']:.3f}ms inference, {speed['postprocess']:.3f}ms postprocess per image")

def extract_box_details(boxes):
    """
    Extract bounding box details from the model's results.

    Args:
        boxes (object): The model's results containing bounding box information.

    Returns:
        tuple: Lists containing xyxy coordinates, confidence scores, class indices, and object IDs.
    """
    xyxy = boxes.xyxy.detach().tolist()
    conf = boxes.conf.detach().tolist()
    cls = boxes.cls.detach().tolist()
    ids = boxes.id.detach().tolist() if hasattr(boxes, 'id') and boxes.id is not None else [None] * len(xyxy)
    return xyxy, conf, cls, ids

def convert_to_yolo_format(x1, y1, x2, y2, width, height):
    """
    Convert bounding box coordinates to YOLO format.

    Args:
        x1 (float): Top-left x coordinate of the bounding box.
        y1 (float): Top-left y coordinate of the bounding box.
        x2 (float): Bottom-right x coordinate of the bounding box.
        y2 (float): Bottom-right y coordinate of the bounding box.
        width (int): Width of the image.
        height (int): Height of the image.

    Returns:
        tuple: Center x, center y, width, and height of the bounding box in YOLO format.
    """
    center_x = (x1 + x2) / 2 / width
    center_y = (y1 + y2) / 2 / height
    box_width = (x2 - x1) / width
    box_height = (y2 - y1) / height
    return center_x, center_y, box_width, box_height

def print_detected_item(classes, class_idx, confidence, x1, y1, x2, y2, obj_id):
    """
    Log the details of a detected item.

    Args:
        classes (list): List of class names.
        class_idx (int): Index of the detected class.
        confidence (float): Confidence score of the detection.
        x1 (float): Top-left x coordinate of the bounding box.
        y1 (float): Top-left y coordinate of the bounding box.
        x2 (float): Bottom-right x coordinate of the bounding box.
        y2 (float): Bottom-right y coordinate of the bounding box.
        obj_id (int): ID of the detected object.
    """
    logging.info(f"Detected item: {classes[class_idx]} with confidence {confidence:.2f} at coordinates ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}), ID: {obj_id}")

def draw_boxes_and_labels(frame, classes, class_idx, confidence, x1, y1, x2, y2, obj_id):
    """
    Draw bounding boxes and labels on the frame.

    Args:
        frame (numpy.ndarray): The image frame to draw on.
        classes (list): List of class names.
        class_idx (int): Index of the detected class.
        confidence (float): Confidence score of the detection.
        x1 (float): Top-left x coordinate of the bounding box.
        y1 (float): Top-left y coordinate of the bounding box.
        x2 (float): Bottom-right x coordinate of the bounding box.
        y2 (float): Bottom-right y coordinate of the bounding box.
        obj_id (int): ID of the detected object.
    """
    # Draw bounding box
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    
    # Draw class label and confidence
    label = f"{classes[class_idx]} {confidence:.2f}"
    cv2.putText(frame, label, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if obj_id is not None:
        id_label = f"ID: {int(obj_id)}"
        cv2.putText(frame, id_label, (int(x1), int(y2 + 30)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        logging.warning("obj_id is None or invalid")
