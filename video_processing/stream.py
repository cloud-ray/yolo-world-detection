# video_processing/stream.py
import cv2
from vidgear.gears import CamGear
from models.yolo_world import YOLOModel
from video_processing.annotators import annotate_frame
from config import FPS

class VideoStream:
    def __init__(self):
        # Initialize CamGear stream
        self.cap = CamGear(
            source="https://www.youtube.com/live/OIqUka8BOS8?si=DVQmFImFtmlBB4QR",
            stream_mode=True,
            logging=True
        ).start()
        
        # Get initial frame to determine width and height
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Unable to read from video source")
        
        height, width, _ = frame.shape
        self.video_info = (width, height, FPS)
        self.model = YOLOModel()

    def generate_frames(self):
        while True:
            frame = self.cap.read()
            if frame is None:
                break
            
            try:
                detections = self.model.infer(frame)
            except AttributeError as e:
                print(e)
                break

            width, height, _ = frame.shape
            detections = detections[detections['confidence'] >= self.model.confidence_threshold]

            labels = [
                f"{detections.iloc[i]['class']} {detections.iloc[i]['confidence']:.3f}"
                for i in range(len(detections))
            ]
            annotated_frame = annotate_frame(frame, detections, labels)
            
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def __del__(self):
        if hasattr(self.cap, 'stop'):
            self.cap.stop()
