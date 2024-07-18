# models/yolo_world.py
import cv2
import supervision as sv
from inference.models.yolo_world.yolo_world import YOLOWorld
from config import MODEL_ID, CLASSES, CONFIDENCE_THRESHOLD, NMS_THRESHOLD

class YOLOModel:
    def __init__(self):
        self.model = YOLOWorld(model_id=MODEL_ID)
        self.model.set_classes(CLASSES)
        self.confidence_threshold = CONFIDENCE_THRESHOLD
        self.nms_threshold = NMS_THRESHOLD

    def infer(self, frame):
        results = self.model.infer(frame, confidence=self.confidence_threshold)
        detections = sv.Detections.from_inference(results).with_nms(threshold=self.nms_threshold)
        return detections
