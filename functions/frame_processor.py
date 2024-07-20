# functions/frame_processor.py
import cv2
import os 

def process_frame(model, classes, frame):
    tracker_config_path = os.path.join('utils', 'bytetrack.yaml')

    results = model.track(frame, tracker=tracker_config_path)
    print(results[0].boxes)

    # Log the speed of the results
    speed = results[0].speed
    print(f"Speed: {speed['preprocess']:.3f}ms preprocess, {speed['inference']:.3f}ms inference, {speed['postprocess']:.3f}ms postprocess per image")

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
    
    return frame







# def process_frame(model, classes, frame, object_tracker, min_consecutive_frames=5, confidence_threshold=0.3):
#     tracker_config_path = os.path.join('utils', 'bytetrack.yaml')

#     results = model.track(frame, tracker=tracker_config_path)
#     print(results[0].boxes)
    
#     # Log the speed of the results
#     speed = results[0].speed
#     print(f"Speed: {speed['preprocess']:.3f}ms preprocess, {speed['inference']:.3f}ms inference, {speed['postprocess']:.3f}ms postprocess per image")

#     current_frame_objects = {}

#     for result in results:
#         boxes = result.boxes
#         xyxy = boxes.xyxy
#         conf = boxes.conf
#         cls = boxes.cls

#         for i in range(len(xyxy)):
#             x1, y1, x2, y2 = xyxy[i]
#             confidence = conf[i]
#             class_idx = int(cls[i])

#             print(f"Detected item: {classes[class_idx]} with confidence {confidence:.2f} at coordinates ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")

#             # Draw bounding box and label
#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f"{classes[class_idx]} {confidence:.2f}", (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
#             if confidence > confidence_threshold:
#                 object_id = (class_idx, int(x1), int(y1), int(x2), int(y2))
#                 current_frame_objects[object_id] = confidence
                
#                 if object_id not in object_tracker:
#                     object_tracker[object_id] = 0
#                 object_tracker[object_id] += 1
                
#                 # Check if the object has been detected for enough consecutive frames
#                 if object_tracker[object_id] >= min_consecutive_frames:
#                     # Print statement for debugging
#                     print(f"Screenshot taken for {classes[class_idx]} with confidence {confidence:.2f} at coordinates ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")
#             else:
#                 # Ensure object_id is initialized before trying to reset
#                 object_id = (class_idx, int(x1), int(y1), int(x2), int(y2))
#                 if object_id in object_tracker:
#                     object_tracker[object_id] = 0

#     # Reset counter for objects not detected in the current frame
#     for obj_id in list(object_tracker.keys()):
#         if obj_id not in current_frame_objects:
#             object_tracker[obj_id] = 0

#     return frame









# def process_frame(model, classes, frame):
#     results = model.predict(frame)
    
#     # Log the speed of the results
#     speed = results[0].speed
#     print(f"Speed: {speed['preprocess']:.3f}ms preprocess, {speed['inference']:.3f}ms inference, {speed['postprocess']:.3f}ms postprocess per image")

#     for result in results:
#         boxes = result.boxes
#         xyxy = boxes.xyxy
#         conf = boxes.conf
#         cls = boxes.cls

#         for i in range(len(xyxy)):
#             x1, y1, x2, y2 = xyxy[i]
#             confidence = conf[i]
#             class_idx = int(cls[i])

#             print(f"Detected item: {classes[class_idx]} with confidence {confidence:.2f} at coordinates ({x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f})")

#             cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(frame, f"{classes[class_idx]} {confidence:.2f}", (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
#     return frame
