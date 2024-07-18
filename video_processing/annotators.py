# video_processing/annotators.py
import supervision as sv

BOUNDING_BOX_ANNOTATOR = sv.BoxAnnotator(thickness=2)
LABEL_ANNOTATOR = sv.LabelAnnotator(text_thickness=2, text_scale=1, text_color=sv.Color.BLACK)

def annotate_frame(frame, detections, labels):
    annotated_frame = frame.copy()
    annotated_frame = BOUNDING_BOX_ANNOTATOR.annotate(annotated_frame, detections)
    annotated_frame = LABEL_ANNOTATOR.annotate(annotated_frame, detections, labels=labels)
    return annotated_frame
