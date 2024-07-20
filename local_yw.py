import cv2
import supervision as sv
from vidgear.gears import CamGear
from ultralytics import YOLO

# Initialize YOLO-World model
model = YOLO("./models/yolov8s-world.pt")

# Set classes for detection
classes = ["bird", "squirrel", "raccoon", "rabbit", "possum", "skunk"]
model.set_classes(classes)

# Initialize CamGear stream
source = "https://www.youtube.com/live/oI8R4_UG3Fs?si=5wyEdbZYlqjgFlmF"
cap = CamGear(source=source, stream_mode=True, logging=True).start()

while True:
    # Read frame from CamGear stream
    frame = cap.read()
    if frame is None:
        break

    # Perform object detection using YOLO-World model
    results = model.predict(frame)

    # Log the speed of the results
    speed = results[0].speed
    print(f"Speed: {speed['preprocess']:.3f}ms preprocess, {speed['inference']:.3f}ms inference, {speed['postprocess']:.3f}ms postprocess per image at shape {(1, 3, 384, 640)}")

    # Draw bounding boxes and labels on the frame
    for result in results:
        boxes = result.boxes
        xyxy = boxes.xyxy
        conf = boxes.conf
        cls = boxes.cls

        for i in range(len(xyxy)):
            x1, y1, x2, y2 = xyxy[i]
            confidence = conf[i]
            class_idx = int(cls[i])

            print(f"Detected item: {classes[class_idx]} with confidence {confidence:.2f} at coordinates ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{classes[class_idx]} {confidence:.2f}", (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the output
    cv2.imshow("YOLO-World Object Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.stop()
cv2.destroyAllWindows()



# WORKS WITHOUT TRACKING
# while True:
#     frame = cap.read()
#     if frame is None:
#         break

#     # Perform inference on the frame
#     results = model.predict(frame, conf=confidence_threshold)[0]
    
#     boxes = results.boxes.xyxy.cpu().numpy()  # Extract bounding boxes
#     confidences = results.boxes.conf.cpu().numpy()  # Extract confidence scores
#     class_ids = results.boxes.cls.cpu().numpy().astype(int)  # Extract class IDs

#     # Convert to supervision Detections format
#     detections = sv.Detections(
#         xyxy=boxes,
#         confidence=confidences,
#         class_id=class_ids
#     ).with_nms(threshold=nms_threshold)

#     # Filter detections by area
#     detections = detections[(detections.area / (width * height)) < 0.10]

#     # Create labels with class names and confidence scores
#     labels = [
#         f"{classes[class_ids[i]]} {confidences[i]:.3f}"
#         for i in range(len(confidences))
#     ]

#     annotated_frame = frame.copy()
    
#     # Annotate bounding boxes
#     annotated_frame = BOUNDING_BOX_ANNOTATOR.annotate(annotated_frame, detections)
    
#     # Annotate labels with confidence scores
#     annotated_frame = LABEL_ANNOTATOR.annotate(annotated_frame, detections, labels=labels)

#     # Display the annotated frame
#     cv2.imshow('frame', annotated_frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break