# utils/frame_utils.py
import time
import logging

class FPSCounter:
    def __init__(self):
        """
        Initializes the FPSCounter instance.

        The FPSCounter tracks the number of frames processed and calculates the
        frames per second (FPS) over time.
        """
        self.start_time = time.time()
        self.frames = 0

    def update(self):
        """
        Updates the FPS counter with a new frame and calculates the FPS if
        one second has passed since the last calculation.

        Returns:
            float: The current FPS if at least one second has passed, otherwise None.
        """
        self.frames += 1
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= 1.0:
            fps = self.frames / elapsed_time
            self.start_time = current_time
            self.frames = 0
            logging.debug(f"FPS calculated: {fps:.2f}")
            return fps
        return None

def throttle_frame_rate(frame, max_fps):
    """
    Throttle the frame rate to achieve a maximum FPS.

    This function ensures that frames are processed at a rate that does not
    exceed the specified maximum FPS. It uses a timestamp to control the
    processing rate and skips frames if necessary.

    Args:
        frame (numpy.ndarray): The image frame to be processed.
        max_fps (float): The maximum FPS to achieve. Frames will be processed
                         only if the time interval since the last processed frame
                         is greater than or equal to 1.0 / max_fps.

    Returns:
        tuple: (throttled_frame, process_frame_flag)
               - throttled_frame: The frame to be processed (may be None if throttled).
               - process_frame_flag: Boolean indicating whether the frame should
                                      be processed (True) or skipped (False).
    """
    current_time = time.time()

    # Initialize last_time if it doesn't exist
    if not hasattr(throttle_frame_rate, "last_time"):
        throttle_frame_rate.last_time = current_time
        logging.debug("Frame processing started.")
        return frame, True

    elapsed_time = current_time - throttle_frame_rate.last_time
    if max_fps and elapsed_time >= 1.0 / max_fps:  # Ensure max_fps is not None
        throttle_frame_rate.last_time = current_time
        logging.debug(f"Frame processed. Elapsed time: {elapsed_time:.3f} seconds.")
        return frame, True

    logging.debug(f"Frame throttled. Elapsed time: {elapsed_time:.3f} seconds.")
    return frame, True  # Return frame and True to continue displaying frames
