# YOLO-World IP Cam: Real-time Object Detection on Your Smartphone

![YOLO-World Detections](./assets/yolo-world-high-thresh.jpg)

**Turn your smartphone into a smart IP camera with real-time object detection powered by YOLO-World!**

This Flask application utilizes the YOLO-World model to detect objects in live video streams from any IP camera, including your phone running the [IP Webcam app](https://play.google.com/store/apps/details?id=com.pas.webcam&pcampaignid=web_share). 

**Here's the magic:**

1. **Your Phone as the Camera:** The IP Webcam app transforms your phone into a wireless IP camera, streaming live video to the application.
2. **YOLO-World in Action:** The YOLO-World model, customized for your needs, detects objects in the video stream in real-time.
3. **Live Object Tracking:** The application analyzes the video frame-by-frame, drawing bounding boxes around objects and tracking them throughout the video.

**Benefits of YOLO-World IP Cam:**

* **Rapid Prototyping:** Quickly get your object detection model up and running with YOLO-World, allowing you to focus on refinement.
* **Continuous Learning:** Capture screenshots of specific objects for ongoing model training, improving its accuracy over time.

## Unleashing the Power of YOLO-World

YOLO-World stands out for its unique "prompt-then-detect" approach. Unlike traditional models limited to predefined categories, YOLO-World detects objects based on descriptive text prompts. This opens up a world of possibilities:

* **Prompt the Model:** Describe the object you want to detect using any text, not just predefined categories.
* **Real-time Detection:** The model leverages your prompt to find the described object in the video stream.

This innovative approach makes YOLO-World a powerful tool for various real-world applications requiring open-vocabulary object detection.



## Table of Contents
1. [Installation and Setup](#installation-and-setup)
   - [Clone the Repository](#clone-the-repository)
   - [Install Dependencies](#install-dependencies)
2. [Configuration](#configuration)
3. [Running the Application](#running-the-application)
4. [Code Overview](#code-overview)
   - [main.py](#mainpy)
   - [Functions Folder](#functions-folder)
   - [Utils Folder](#utils-folder)
5. [License](#license)
6. [Acknowledgments](#acknowledgments)
7. [Contact](#contact)

## Installation and Setup

### Clone the Repository

Clone the repository and switch to the feature branch:

```bash
git clone https://github.com/cloud-ray/yolo-world-detection.git
cd yolo-world-detection
git checkout feature/youtube-live
```

### Install Dependencies

Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

Update the `utils/config.py` file with the necessary paths and settings:

### Paths and Model Settings
```python
# Path to the YOLO model file
MODEL_PATH = "path/to/your/model/file"

# List of class names for the model
MODEL_CLASSES = ["class1", "class2", "class3"]

# Path to the video source or camera URL
VIDEO_SOURCE = "path/to/your/video/source"
```

### Key Configuration Values
```python
# Flag to determine whether to save annotated images or clean images
SAVE_ANNOTATED_IMAGES = True
```
- **`SAVE_ANNOTATED_IMAGES`**: When set to `True`, saves images with bounding boxes. Set to `False` for clean images without annotations.

```python
# Interval in seconds between detections
DETECTION_INTERVAL = 0
```
- **`DETECTION_INTERVAL`**: Controls detection frequency. `0` performs detection on every frame. Increase to reduce processing load.

```python
# Maximum number of frames per second to process
FPS = 30
```
- **`FPS`**: Sets the maximum frames per second. Lower FPS reduces processing load but may affect video smoothness. Adjust according to your needs.

## Running the Application

Start the application with:

```bash
python main.py
```

### Usage
- The application initializes the YOLO model and video stream.
- It processes frames in real-time and displays the output.
- Press 'q' to quit the application.

### Troubleshooting
- Ensure all paths in `utils/config.py` are correct.
- Check logs for errors or warnings. Refer to `utils/logger.py` for logging details.

## Code Overview

### `main.py`

The `main.py` file orchestrates the object detection application:

- **Setup Logging**: Configures logging.
- **Load Model**: Initializes the YOLO-World object detection model.
- **Initialize Stream**: Starts video capture.
- **Process and Display Frames**: Processes and displays video frames.
- **Cleanup**: Releases resources and closes windows.

### Functions Folder

- **`frame_processor.py`**: Processes frames for detection and tracking.
- **`object_tracker.py`**: Tracks detected objects.
- **`screenshot_handler.py`**: Manages screenshots and labels.
- **`stream_handler.py`**: Manages video streams.
- **`yolo_model.py`**: Configures and loads the YOLO model.

### Utils Folder

- **`config.py`**: Manages configuration settings.
- **`frame_utils.py`**: Provides utilities for frame processing.
- **`logger.py`**: Configures application logging.
- **`image_utils.py`**: Handles image processing tasks.
- **`annotator.py`**: Processes images with annotations.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [YOLO-World Model](https://docs.ultralytics.com/models/yolo-world)
- [How to Detect Objects with YOLO-World](https://blog.roboflow.com/how-to-detect-objects-with-yolo-world/)
- [Object Counting using Ultralytics YOLOv8](https://docs.ultralytics.com/guides/object-counting/)

## Contact

For any questions or comments, please contact [Ray](mailto:ray@cybersavvy.one).
