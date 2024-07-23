# functions/object_tracker.py

# Utility imports
import logging
from utils.logger import setup_logging

# Configuration imports
from utils.config import SS_CONFIDENCE_THRESHOLD

# Set up logging
setup_logging()

# Global state tracker
object_tracker = {}

def initialize_object_tracker():
    """
    Initialize the global object tracker dictionary.
    
    This function resets the global object tracker, clearing all previously
    tracked objects and logging the initialization event.
    """
    global object_tracker
    object_tracker = {}
    logging.info("Object tracker initialized.")


def update_object_tracker(obj_id, confidence):
    """
    Update the object tracker with new data for a specific object.

    Args:
        obj_id (int): The ID of the object to update.
        confidence (float): The confidence score of the detected object.
    
    Updates the tracker for the object with the given `obj_id`. If the object
    is new, it initializes its data. If the object already exists, it updates
    the confidence values and frame count based on the provided `confidence`.
    If the confidence is below the configured threshold, it resets the frame
    count and timer for screenshots.
    """
    global object_tracker

    if obj_id not in object_tracker:
        object_tracker[obj_id] = {
            'confidence_values': [confidence],
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
            # Reset frame count and screenshot timer if confidence is below threshold
            object_tracker[obj_id]['frame_count'] = 0
            object_tracker[obj_id]['frames_since_last_screenshot'] = 0
            logging.debug(f"Object {obj_id} confidence below threshold. Resetting frame count and screenshot timer.")


def log_object_tracker_summary(obj_id):
    """
    Log a summary of the tracked data for a specific object.

    Args:
        obj_id (int): The ID of the object to summarize.
    
    Logs the total frame count, and whether all confidence values for the object
    are consistently above the configured threshold.
    """
    if obj_id in object_tracker:
        obj_data = object_tracker[obj_id]
        confidence_values = obj_data['confidence_values']
        frame_count = obj_data['frame_count']
        threshold = SS_CONFIDENCE_THRESHOLD
        # logging.info(f"Object ID: {obj_id}")
        logging.info(f"FRAME_COUNT_THRESHOLD: {frame_count}")
        # Checking if all confidence values are above the threshold
        all_above_threshold = all(c > threshold for c in confidence_values)
        logging.info(f"Consistent above threshold: {all_above_threshold}")
    else:
        logging.warning(f"Object ID {obj_id} not found in tracker.")
