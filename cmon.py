import os
import cv2
from vidgear.gears import CamGear
from ultralytics import YOLO

# Initialize YOLO-World model
model = YOLO("./models/yolov8s-world.pt")

# Set classes for detection
classes = ["bird", "box", "plant", "flowers"]
model.set_classes(classes)

# Initialize CamGear stream
source = "https://www.youtube.com/live/4kRzwJXaeIM?si=SyCTMoIGJfCMZcF7"
cap = CamGear(source=source, stream_mode=True, logging=True).start()

# tracker_config_path = os.path.join('utils', 'bytetrack.yaml')

while True:
    # Read frame from stream
    frame = cap.read()
    if frame is None:
        break

    # Track objects in the frame
    results = model.track(
        source=frame, 
        persist=True, 
        tracker="./utils/bytetrack.yaml", 
        conf=0.5, 
        iou=0.5, 
        classes=14, 
        verbose=True 
    )

    print(results[0].boxes)

    # Display the output
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
cv2.destroyAllWindows()