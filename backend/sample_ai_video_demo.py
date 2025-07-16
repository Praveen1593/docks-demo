import cv2
from object_detector import ObjectDetector
from emotion_detector import EmotionDetector
import os

# Path to your test video file
VIDEO_PATH = "sample_video.mp4"  # Replace with your video file
ALERT_OUTPUT_DIR = "alerts_output"

# Create output directory for alert frames
os.makedirs(ALERT_OUTPUT_DIR, exist_ok=True)

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    object_detector = ObjectDetector()
    emotion_detector = EmotionDetector()
    frame_count = 0
    alert_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Object detection
        objects = object_detector.detect_objects(frame, confidence_threshold=0.5)
        person_detected = any(obj['class_name'] == 'person' for obj in objects)

        # Emotion detection
        emotions = emotion_detector.detect_emotions(frame, confidence_threshold=0.7)
        angry_detected = any(e['emotion'] == 'angry' for e in emotions)

        # Draw annotations
        annotated = object_detector.draw_object_annotations(frame, objects)
        annotated = emotion_detector.draw_emotion_annotations(annotated, emotions)

        # Show the frame
        cv2.imshow("Obscure Eye AI Demo", annotated)

        # Alert logic: if person or angry detected, save frame and print alert
        if person_detected or angry_detected:
            alert_count += 1
            alert_type = []
            if person_detected:
                alert_type.append("Person")
            if angry_detected:
                alert_type.append("Angry Emotion")
            print(f"[ALERT] Frame {frame_count}: {', '.join(alert_type)} detected!")
            out_path = os.path.join(ALERT_OUTPUT_DIR, f"alert_{frame_count}.jpg")
            cv2.imwrite(out_path, annotated)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nProcessed {frame_count} frames. {alert_count} alerts triggered.")
    print(f"Alert frames saved in: {ALERT_OUTPUT_DIR}")

if __name__ == "__main__":
    main()