# functions/object_tracker.py
import logging
from utils.logger import setup_logging
from utils.config import SS_CONFIDENCE_THRESHOLD, FRAME_COUNT_THRESHOLD, ADDITIONAL_FRAME_THRESHOLD, MAX_SCREENSHOTS

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
            'initial_saved': False,  # Flag for initial screenshot
            'screenshot_count': 0,  # Number of screenshots saved
            'track': True  # Flag to indicate if the object is still tracked
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

        # Calculate summary statistics
        min_confidence = min(confidence_values)
        max_confidence = max(confidence_values)
        avg_confidence = sum(confidence_values) / len(confidence_values) if confidence_values else 0
        above_threshold_count = sum(1 for c in confidence_values if c > threshold)

        # Log summary
        logging.info(f"Object ID: {obj_id}")
        logging.info(f"FRAME_COUNT_THRESHOLD: {frame_count}")
        logging.info(f"Minimum Confidence: {min_confidence:.2f}")
        logging.info(f"Maximum Confidence: {max_confidence:.2f}")
        logging.info(f"Average Confidence: {avg_confidence:.2f}")
        logging.info(f"Count Above Threshold ({threshold}): {above_threshold_count}")
        logging.info(f"Consistent above threshold: {all(c > threshold for c in confidence_values)}")
    else:
        logging.warning(f"Object ID {obj_id} not found in tracker.")
