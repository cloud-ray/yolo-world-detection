# utils/config.py

# Configuration settings for the object detection and tracking system

# Object detection and tracking thresholds
MODEL_TRACK_CONF = 0.25  # Minimum confidence threshold for object detection
MODEL_TRACK_IOU = 0.5    # Minimum intersection over union (IOU) threshold for object tracking

SS_CONFIDENCE_THRESHOLD = 0.25  # Confidence threshold for object detection before saving a screenshot
FRAME_COUNT_THRESHOLD = 3  # Number of consecutive frames required to save a screenshot
ADDITIONAL_FRAME_THRESHOLD = 20  # Number of frames before saving additional screenshots
MAX_SCREENSHOTS = 5 # Maximum number of screenshots to save

RESIZE_DIMENSIONS = (1280, 720) # Resize dimensions for images (width, height)
JPEG_QUALITY = 90 # JPEG quality setting for saved screenshots (1-100)


SQLITE_DATABASE_PATH = 'database/database.db'



# Frame rate (FPS) settings
# This controls the maximum number of frames per second to process.
# Lower FPS can help reduce processing load but may affect smoothness of the video stream.
# Common values are 15, 30, or 60 FPS depending on your application's performance needs.
FPS = 30

PLOT_ANNOTATED_BOXES = True  # Set to False if you do not want to plot annotated boxes on the images

# Detection interval settings
DETECTION_INTERVAL = 1  # Interval in seconds between detections

# Paths to configuration files
TRACKER_CONFIG_PATH = "./config/bytetrack.yaml"  # Path to the tracker configuration file

# Model and video source configurations
MODEL_PATH = "./model/yolov8s-world.pt"  # Path to the YOLO model file
MODEL_CLASSES = ["bird", "squirrel", "deer", "raccoon"]  # List of class names for the model
VIDEO_SOURCE = "https://www.youtube.com/live/OIqUka8BOS8?si=56OndqNXGyWHC0kT"  # URL or path of the video source

# Logging configurations
LOG_DIRECTORY = "logs"  # Directory where log files will be saved
LOG_FILE_NAME = "application.log"  # Name of the log file

# Screenshot configurations
ORIGINAL_SCREENSHOT_DIRECTORY = "screenshots/original/screenshots"
ORIGINAL_LABELS_DIRECTORY = "screenshots/original/labels"

ORIGINAL_JSON_DIRECTORY = "screenshots/original/json"
ORIGINAL_JSON_FILE_NAME = "original_screenshot_data.json"



RESIZED_WITH_BBOX_DIRECTORY = "screenshots/resized/with_bbox"
RESIZED_WITHOUT_BBOX_DIRECTORY = "screenshots/resized/without_bbox"
RESIZED_LABELS_DIRECTORY = "screenshots/resized/labels"




LABEL_DIRECTORY = "screenshots/labels"
ANNOTATE_DIRECTORY = "screenshots/annotated"