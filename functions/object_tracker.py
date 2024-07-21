# functions/object_tracker.py
import logging
from utils.logger import setup_logging
from utils.config import SS_CONFIDENCE_THRESHOLD

# Set up logging
setup_logging()

# Global state tracker
object_tracker = {}

def initialize_object_tracker():
    """
    Initialize the global object tracker state.
    """
    global object_tracker
    object_tracker = {}
    logging.info("Object tracker initialized.")

initialize_object_tracker()

def update_object_tracker(obj_id, confidence):
    """
    Update the state of the object tracker with the given object ID and confidence.
    
    Args:
        obj_id (int): The ID of the object being tracked.
        confidence (float): The confidence score of the detected object.
    """
    global object_tracker

    if obj_id not in object_tracker:
        object_tracker[obj_id] = {
            'confidence_values': [confidence],  # Store confidence values
            'frame_count': 1,
            'frames_since_last_screenshot': 0,
            'saved': False
        }
        logging.info(f"Object {obj_id} initialized with confidence {confidence:.2f}.")
    else:
        if confidence > SS_CONFIDENCE_THRESHOLD:
            object_tracker[obj_id]['frame_count'] += 1
            object_tracker[obj_id]['confidence_values'].append(confidence)
            object_tracker[obj_id]['frames_since_last_screenshot'] += 1
            logging.debug(f"Object {obj_id} updated: confidence {confidence:.2f}, frame count {object_tracker[obj_id]['frame_count']}.")
        else:
            object_tracker[obj_id]['frame_count'] = 0
            object_tracker[obj_id]['frames_since_last_screenshot'] = 0
            logging.debug(f"Object {obj_id} confidence below threshold. Resetting frame count and screenshot timer.")

def log_object_tracker_summary(obj_id):
    """
    Log a summary of the object tracker data, including confidence values and frame count threshold.
    
    Args:
        obj_id (int): The ID of the object being tracked.
    """
    if obj_id in object_tracker:
        obj_data = object_tracker[obj_id]
        confidence_values = obj_data['confidence_values']
        frame_count = obj_data['frame_count']
        threshold = SS_CONFIDENCE_THRESHOLD
        logging.info(f"Object ID: {obj_id}")
        logging.info(f"FRAME_COUNT_THRESHOLD: {frame_count}")
        # logging.info(f"Confidence values: {confidence_values}")
        logging.info(f"Consistent above threshold: {all(c > threshold for c in confidence_values)}")
    else:
        logging.warning(f"Object ID {obj_id} not found in tracker.")
