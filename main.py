import cv2
from functions.yolo_model import initialize_model
from functions.stream_handler import initialize_stream
from functions.frame_processor import process_frame

def main():
    # Initialize YOLO-World model
    model_path = "./models/yolov8s-world.pt"
    classes = ["bird", "squirrel", "raccoon", "rabbit", "possum", "skunk", "deer"]
    model = initialize_model(model_path, classes)

    # Initialize CamGear stream
    source = "https://www.youtube.com/live/4kRzwJXaeIM?si=SyCTMoIGJfCMZcF7"
    cap = initialize_stream(source)

    while True:
        # Read frame from CamGear stream
        frame = cap.read()
        if frame is None:
            break

        # Process the frame
        frame = process_frame(model, classes, frame)

        # Display the output
        cv2.imshow("YOLO-World Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
