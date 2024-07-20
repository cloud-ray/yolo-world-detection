# utils/config.py

# Configuration settings for the object detection and tracking system

# Object detection and tracking thresholds
MODEL_TRACK_CONF = 0.25  # Minimum confidence threshold for object detection
MODEL_TRACK_IOU = 0.5    # Minimum intersection over union (IOU) threshold for object tracking
SS_CONFIDENCE_THRESHOLD = 0.5  # Confidence threshold for object detection before saving a screenshot
FRAME_COUNT_THRESHOLD = 3  # Number of consecutive frames required to save a screenshot
ADDITIONAL_FRAME_THRESHOLD = 20  # Number of frames before saving additional screenshots
MAX_SCREENSHOTS = 5


# Frame rate (FPS) settings
# This controls the maximum number of frames per second to process.
# Lower FPS can help reduce processing load but may affect smoothness of the video stream.
# Common values are 15, 30, or 60 FPS depending on your application's performance needs.
FPS = 30

# Detection interval settings
DETECTION_INTERVAL = 1  # Interval in seconds between detections

# Paths to configuration files
TRACKER_CONFIG_PATH = "./config/bytetrack.yaml"  # Path to the tracker configuration file

# Model and video source configurations
MODEL_PATH = "./model/yolov8s-world.pt"  # Path to the YOLO model file
MODEL_CLASSES = ["bird", "squirrel", "deer"]  # List of class names for the model
VIDEO_SOURCE = "https://www.youtube.com/live/2uabwdYMzVk?si=2aB8m5P6SCxCRUPY"  # URL or path of the video source

# Logging configurations
LOG_DIRECTORY = "logs"  # Directory where log files will be saved
LOG_FILE_NAME = "application.log"  # Name of the log file

# Screenshot configurations
IMAGE_DIRECTORY = "./screenshots/images"
LABEL_DIRECTORY = "./screenshots/labels"
ANNOTATE_DIRECTORY = "./screenshots/annotated"