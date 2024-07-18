VIDEO_SOURCE = "http://192.168.4.24:8080/video"
MODEL_ID = "yolo_world/s"
CLASSES = ["book", "shoe", "table", "pillow", "toy", "stuffed animal"]

# Confidence threshold: minimum confidence score required for a detection to be considered valid
# Lower values (e.g. 0.01) will detect more objects, but may include false positives
# Higher values (e.g. 0.5) will detect fewer objects, but with higher accuracy
CONFIDENCE_THRESHOLD = 0.3

# Non-maximum suppression (NMS) threshold: controls how similar two detections need to be to be merged
# Lower values (e.g. 0.01) will merge very similar detections, reducing the number of objects detected
# Higher values (e.g. 0.5) will merge detections that are quite dissimilar, resulting in more objects detected
NMS_THRESHOLD = 0.03

FPS = 30
