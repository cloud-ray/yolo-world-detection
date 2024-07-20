from ultralytics import YOLO
import cv2
import os

# Initialize YOLO model
model = YOLO("./models/yolov8s-world.pt")

# Define custom classes
model.set_classes(["person", "bus"])

# Path to the tracker configuration file
tracker_config_path = os.path.join('utils', 'bytetrack.yaml')

def track_objects(youtube_stream):
    while True:
        frame = youtube_stream.read()
        if frame is None:
            break

        # Track objects with YOLO
        results = model.track(
            source=frame, # source directory for images or videos
            persist=True, # persisting tracks between frames
            tracker=tracker_config_path, # Tracking method 'bytetrack' or 'botsort'
            conf=0.5, # Confidence Threshold
            iou=0.5, # IOU Threshold
            classes=[14], # filter results by class, i.e. classes=0, or classes=[0,2,3]
            verbose=True # Display the object tracking results
        )
        annotated_frame = results[0].plot()  # Annotate frame with bounding boxes and labels

        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
