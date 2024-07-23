# main.py
import cv2
import logging
import time
from yolo_model import initialize_model
from stream_handler import initialize_stream
from functions.frame_processor import process_frame
from utils.config import MODEL_PATH, MODEL_CLASSES, VIDEO_SOURCE, FPS
from utils.logger import setup_logging

# Desired frame rate (e.g., 30 FPS)
desired_fps = FPS
frame_time = 1.0 / desired_fps

def main(): 
    # Set up logging
    setup_logging()

    # Initialize YOLO-World model
    model_path = MODEL_PATH
    classes = MODEL_CLASSES
    model = initialize_model(model_path, classes)
    if model is None:
        logging.error("Failed to initialize model.")
        return

    # Initialize CamGear stream
    source = VIDEO_SOURCE
    cap = initialize_stream(source)
    if cap is None:
        logging.error("Failed to initialize stream.")
        return

    try:
        while True:
            start_time = time.time()

            # Read frame from CamGear stream
            frame = cap.read()
            if frame is None:
                logging.warning("No frame received from stream.")
                break

            # Process the frame
            frame = process_frame(model, classes, frame)

            # Display the output
            cv2.imshow("YOLO-World Object Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Calculate the time taken to process and display the frame
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Sleep for the remaining time to match the desired frame rate
            sleep_time = max(0, frame_time - elapsed_time)
            time.sleep(sleep_time)
    finally:
        # Release resources
        cap.stop()
        cv2.destroyAllWindows()
        logging.info("Released resources and closed windows.")

if __name__ == "__main__":
    main()
