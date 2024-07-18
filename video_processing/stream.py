# video_processing/stream.py
import cv2
from models.yolo_world import YOLOModel
from video_processing.annotators import annotate_frame
from config import VIDEO_SOURCE, FPS

class VideoStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not self.cap.isOpened():
            raise RuntimeError("Unable to open video source")
        
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Unable to read video source")
        
        height, width, _ = frame.shape
        self.video_info = (width, height, FPS)
        self.model = YOLOModel()

    def generate_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            try:
                detections = self.model.infer(frame)
            except AttributeError as e:
                print(e)
                break

            width, height, _ = frame.shape
            detections = detections[(detections.area / (width * height)) < 0.10]

            labels = [
                f"{detections.data['class_name'][i]} {detections.confidence[i]:.3f}"
                for i in range(len(detections.confidence))
            ]
            annotated_frame = annotate_frame(frame, detections, labels)
            
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
