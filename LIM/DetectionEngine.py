import time
from threading import Thread
import cv2
from ultralytics import YOLO

class DetectionEngine:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
    
    def detect(self, source: int, callback) -> dict:
        T = Thread(target=self.__detect__, args=(source, callback), daemon=True)
        T.start()

    def __detect__(self, source, callback):
        capture = cv2.VideoCapture(source)

        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                results = self.model(source=frame, conf=0.2, iou=0.5, max_det=10, verbose=False)
                callback(frame, results)
            
            time.sleep(2)
        
        capture.release()