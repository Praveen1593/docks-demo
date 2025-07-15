import cv2
import numpy as np
from fer import FER
import mediapipe as mp
from typing import List, Tuple, Dict

class EmotionDetector:
    """Emotion detection using facial expression recognition"""
    
    def __init__(self):
        """Initialize the emotion detector"""
        self.fer_detector = FER(mtcnn=True)
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5
        )
        
        # Emotion mapping for better readability
        self.emotion_labels = {
            'angry': 'Angry',
            'disgust': 'Disgust',
            'fear': 'Fear',
            'happy': 'Happy',
            'sad': 'Sad',
            'surprise': 'Surprise',
            'neutral': 'Neutral'
        }
        
    def detect_emotions(self, frame: np.ndarray, confidence_threshold: float = 0.7) -> List[Dict]:
        """
        Detect emotions in the given frame
        
        Args:
            frame: Input frame from camera
            confidence_threshold: Minimum confidence for emotion detection
            
        Returns:
            List of detected emotions with bounding boxes and confidence scores
        """
        emotions_detected = []
        
        try:
            # Use FER for emotion detection
            fer_results = self.fer_detector.detect_emotions(frame)
            
            for face_data in fer_results:
                box = face_data["box"]
                emotions = face_data["emotions"]
                
                # Find the dominant emotion
                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion]
                
                if confidence >= confidence_threshold:
                    emotions_detected.append({
                        'emotion': dominant_emotion,
                        'confidence': confidence,
                        'bounding_box': box,
                        'all_emotions': emotions
                    })
                    
        except Exception as e:
            print(f"⚠️ Error in emotion detection: {e}")
            
        return emotions_detected
    
    def draw_emotion_annotations(self, frame: np.ndarray, emotions: List[Dict]) -> np.ndarray:
        """
        Draw emotion annotations on the frame
        
        Args:
            frame: Input frame
            emotions: List of detected emotions
            
        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()
        
        for emotion_data in emotions:
            box = emotion_data['bounding_box']
            emotion = emotion_data['emotion']
            confidence = emotion_data['confidence']
            
            # Extract bounding box coordinates
            x, y, w, h = box
            
            # Draw rectangle around face
            color = self._get_emotion_color(emotion)
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw emotion label
            label = f"{self.emotion_labels.get(emotion, emotion)}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            
            # Background for text
            cv2.rectangle(annotated_frame, 
                         (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), 
                         color, -1)
            
            # Text
            cv2.putText(annotated_frame, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
        return annotated_frame
    
    def _get_emotion_color(self, emotion: str) -> Tuple[int, int, int]:
        """Get color for emotion visualization"""
        emotion_colors = {
            'angry': (0, 0, 255),      # Red
            'fear': (255, 0, 255),     # Magenta
            'sad': (255, 0, 0),        # Blue
            'disgust': (0, 128, 0),    # Dark Green
            'surprise': (0, 255, 255), # Yellow
            'happy': (0, 255, 0),      # Green
            'neutral': (128, 128, 128) # Gray
        }
        return emotion_colors.get(emotion, (255, 255, 255))  # Default white
    
    def is_alert_emotion(self, emotion: str, alert_emotions: List[str]) -> bool:
        """Check if detected emotion should trigger an alert"""
        return emotion.lower() in [e.lower().strip() for e in alert_emotions]
    
    def get_alert_emotions(self, emotions: List[Dict], alert_emotions: List[str]) -> List[Dict]:
        """Filter emotions that should trigger alerts"""
        alert_list = []
        for emotion_data in emotions:
            if self.is_alert_emotion(emotion_data['emotion'], alert_emotions):
                alert_list.append(emotion_data)
        return alert_list