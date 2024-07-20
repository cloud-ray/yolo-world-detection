from ultralytics import YOLO

def initialize_model(model_path, classes):
    model = YOLO(model_path)
    model.set_classes(classes)
    return model
