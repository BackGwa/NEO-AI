from Detectify import Predict

class DetectionEngine:
    def __init__(self, model_path: str):
        self.pre = Predict(model_path)
        self.pre.max_objs = 10
        self.pre.iou = 0.5
    
    