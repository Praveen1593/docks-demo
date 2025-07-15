import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Tuple

class ObjectDetector:
    """Object detection using YOLOv8"""
    
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Initialize the object detector
        
        Args:
            model_path: Path to YOLO model (will download if not exists)
        """
        try:
            self.model = YOLO(model_path)
            print(f"✅ Loaded YOLO model: {model_path}")
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            self.model = None
            
        # Common COCO class names
        self.class_names = {
            0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane',
            5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light',
            10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
            14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow',
            20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
            25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee',
            30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat',
            35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
            39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife',
            44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
            49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
            54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant',
            59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop',
            64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave',
            69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book',
            74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier',
            79: 'toothbrush'
        }
        
    def detect_objects(self, frame: np.ndarray, confidence_threshold: float = 0.5) -> List[Dict]:
        """
        Detect objects in the given frame
        
        Args:
            frame: Input frame from camera
            confidence_threshold: Minimum confidence for object detection
            
        Returns:
            List of detected objects with bounding boxes and confidence scores
        """
        if self.model is None:
            return []
            
        objects_detected = []
        
        try:
            # Run inference
            results = self.model(frame, verbose=False)
            
            # Process results
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get box coordinates and confidence
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        
                        if confidence >= confidence_threshold:
                            class_name = self.class_names.get(class_id, f"class_{class_id}")
                            
                            objects_detected.append({
                                'class_name': class_name,
                                'class_id': class_id,
                                'confidence': float(confidence),
                                'bounding_box': [int(x1), int(y1), int(x2), int(y2)]
                            })
                            
        except Exception as e:
            print(f"⚠️ Error in object detection: {e}")
            
        return objects_detected
    
    def draw_object_annotations(self, frame: np.ndarray, objects: List[Dict]) -> np.ndarray:
        """
        Draw object annotations on the frame
        
        Args:
            frame: Input frame
            objects: List of detected objects
            
        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()
        
        for obj in objects:
            x1, y1, x2, y2 = obj['bounding_box']
            class_name = obj['class_name']
            confidence = obj['confidence']
            
            # Draw rectangle
            color = self._get_class_color(obj['class_id'])
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            
            # Background for text
            cv2.rectangle(annotated_frame, 
                         (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), 
                         color, -1)
            
            # Text
            cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
        return annotated_frame
    
    def _get_class_color(self, class_id: int) -> Tuple[int, int, int]:
        """Generate a color for each class"""
        np.random.seed(class_id)
        color = np.random.randint(0, 255, size=3)
        return tuple(map(int, color))
    
    def is_alert_object(self, class_name: str, alert_objects: List[str]) -> bool:
        """Check if detected object should trigger an alert"""
        return class_name.lower() in [obj.lower().strip() for obj in alert_objects]
    
    def get_alert_objects(self, objects: List[Dict], alert_objects: List[str]) -> List[Dict]:
        """Filter objects that should trigger alerts"""
        alert_list = []
        for obj in objects:
            if self.is_alert_object(obj['class_name'], alert_objects):
                alert_list.append(obj)
        return alert_list
    
    def count_objects_by_class(self, objects: List[Dict]) -> Dict[str, int]:
        """Count detected objects by class"""
        counts = {}
        for obj in objects:
            class_name = obj['class_name']
            counts[class_name] = counts.get(class_name, 0) + 1
        return counts