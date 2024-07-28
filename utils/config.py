# utils/config.py

# Configuration settings for the object detection and tracking system

# Object Detection and Tracking
MODEL_TRACK_CONF = 0.25  # Minimum confidence threshold for object detection
MODEL_TRACK_IOU = 0.5    # Minimum intersection over union (IOU) threshold for object tracking

# Screenshot Settings
SS_CONFIDENCE_THRESHOLD = 0.25  # Confidence threshold for object detection before saving a screenshot
FRAME_COUNT_THRESHOLD = 3  # Number of consecutive frames required to save a screenshot
ADDITIONAL_FRAME_THRESHOLD = 20  # Number of frames before saving additional screenshots
MAX_SCREENSHOTS = 5  # Maximum number of screenshots to save

# Image Processing
IMAGE_QUALITY = 90 # JPEG quality setting for saved screenshots (1-100)
NEW_IMAGE_SIZE_HEIGHT = 720
NEW_IMAGE_SIZE_WIDTH = 1280

# Database
SQLITE_DATABASE_PATH = 'database/database.db'

# Frame Rate (FPS) Settings
FPS = 30  # Controls the maximum number of frames per second to process

# Plotting Settings
PLOT_ANNOTATED_BOXES = True  # Set to False if you do not want to plot annotated boxes on the images

# Detection Interval Settings
DETECTION_INTERVAL = 1  # Interval in seconds between detections

# Configuration File Paths
TRACKER_CONFIG_PATH = "./config/bytetrack.yaml"  # Path to the tracker configuration file

# Model and Video Source Configurations
MODEL_PATH = "./model/yolov8s-world.pt"  # Path to the YOLO model file
MODEL_CLASSES = ["sofa chair", "lamp", "teapot"]  # List of class names for the model
VIDEO_SOURCE = "https://www.youtube.com/live/x10vL6_47Dw?si=Mv-dGI0rM2Egk2Uf"  # URL or path of the video source

# Logging Configurations
LOG_DIRECTORY = "logs"  # Directory where log files will be saved
LOG_FILE_NAME = "application.log"  # Name of the log file

# Screenshot Directories
ORIGINAL_SCREENSHOT_DIRECTORY = "screenshots/original/screenshots"
ORIGINAL_LABELS_DIRECTORY = "screenshots/original/labels"

ORIGINAL_YOLO_CONFIRMATION_DIRECTORY = "screenshots/original/yolo_bbox"
RESIZED_YOLO_CONFIRMATION_DIRECTORY = "screenshots/resized/yolo_bbox"

RESIZED_WITH_BBOX_DIRECTORY = "screenshots/resized/with_bbox"
RESIZED_WITHOUT_BBOX_DIRECTORY = "screenshots/resized/without_bbox"
RESIZED_LABELS_DIRECTORY = "screenshots/resized/labels"



RESIZED_WITHOUT_BBOX_DIRECTORY = "./screenshots/resized/without_bbox"
RESIZED_WITH_BBOX_DIRECTORY = "./screenshots/resized/with_bbox"