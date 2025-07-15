#!/usr/bin/env python3
"""
Custom Model Training System for Theft Detection
"""

import os
import cv2
import numpy as np
import json
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import shutil
import yaml

# Deep learning imports
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    import torchvision.transforms as transforms
    from ultralytics import YOLO
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("⚠️ PyTorch not available - using YOLOv8 training only")

class TheftDatasetManager:
    """Manage training data for theft detection"""
    
    def __init__(self, data_dir: str = "theft_training_data"):
        self.data_dir = Path(data_dir)
        self.images_dir = self.data_dir / "images"
        self.labels_dir = self.data_dir / "labels"
        self.annotations_file = self.data_dir / "annotations.json"
        
        # Create directory structure
        self._create_directory_structure()
        
        # Initialize annotations
        self.annotations = self._load_annotations()
        
        print(f"📁 Dataset manager initialized: {self.data_dir}")
    
    def _create_directory_structure(self):
        """Create training data directory structure"""
        directories = [
            self.data_dir,
            self.images_dir,
            self.labels_dir,
            self.data_dir / "train" / "images",
            self.data_dir / "train" / "labels",
            self.data_dir / "val" / "images",
            self.data_dir / "val" / "labels",
            self.data_dir / "test" / "images",
            self.data_dir / "test" / "labels"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print("✅ Created training data directory structure")
    
    def _load_annotations(self) -> Dict:
        """Load existing annotations"""
        if self.annotations_file.exists():
            with open(self.annotations_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'theft_scenarios': [],
                'normal_scenarios': [],
                'suspicious_behaviors': [],
                'objects': [],
                'metadata': {
                    'created': datetime.now().isoformat(),
                    'version': '1.0',
                    'classes': [
                        'person',
                        'suspicious_person',
                        'thief',
                        'bag',
                        'valuable_item',
                        'weapon',
                        'stolen_object'
                    ]
                }
            }
    
    def save_annotations(self):
        """Save annotations to file"""
        with open(self.annotations_file, 'w') as f:
            json.dump(self.annotations, f, indent=2)
        print("💾 Annotations saved")
    
    def capture_training_data(self, camera_index: int = 0, scenario_type: str = 'normal'):
        """
        Interactive training data capture
        
        Args:
            camera_index: Camera device index
            scenario_type: 'normal', 'theft', 'suspicious'
        """
        print(f"📸 Starting training data capture for '{scenario_type}' scenarios")
        print("Controls:")
        print("  SPACE - Capture image")
        print("  S - Mark as suspicious behavior")
        print("  T - Mark as theft scenario")
        print("  N - Mark as normal scenario")
        print("  Q - Quit capture")
        
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"❌ Cannot open camera {camera_index}")
            return
        
        capture_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read frame")
                break
            
            # Display frame with instructions
            display_frame = frame.copy()
            cv2.putText(display_frame, f"Scenario: {scenario_type.upper()}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Captured: {capture_count}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(display_frame, "SPACE=Capture, S=Suspicious, T=Theft, N=Normal, Q=Quit", 
                       (10, frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow('Training Data Capture', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):  # Space - capture
                self._save_training_image(frame, scenario_type, capture_count)
                capture_count += 1
                print(f"📸 Captured image {capture_count}")
                
            elif key == ord('s'):  # Mark as suspicious
                scenario_type = 'suspicious'
                print("🔍 Switched to suspicious behavior capture")
                
            elif key == ord('t'):  # Mark as theft
                scenario_type = 'theft'
                print("🚨 Switched to theft scenario capture")
                
            elif key == ord('n'):  # Mark as normal
                scenario_type = 'normal'
                print("✅ Switched to normal scenario capture")
                
            elif key == ord('q'):  # Quit
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"✅ Capture completed - {capture_count} images saved")
        self.save_annotations()
    
    def _save_training_image(self, frame: np.ndarray, scenario_type: str, image_id: int):
        """Save training image with metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{scenario_type}_{timestamp}_{image_id:04d}.jpg"
        image_path = self.images_dir / filename
        
        # Save image
        cv2.imwrite(str(image_path), frame)
        
        # Create annotation entry
        annotation = {
            'filename': filename,
            'scenario_type': scenario_type,
            'timestamp': timestamp,
            'image_id': image_id,
            'width': frame.shape[1],
            'height': frame.shape[0],
            'objects': [],  # To be filled by annotation tool
            'behaviors': []  # To be filled by annotation tool
        }
        
        # Add to appropriate category
        if scenario_type == 'theft':
            self.annotations['theft_scenarios'].append(annotation)
        elif scenario_type == 'suspicious':
            self.annotations['suspicious_behaviors'].append(annotation)
        else:
            self.annotations['normal_scenarios'].append(annotation)
    
    def annotate_images_interactive(self):
        """Interactive image annotation tool"""
        print("🖼️ Starting interactive annotation")
        print("Controls:")
        print("  Click and drag to draw bounding boxes")
        print("  1-7: Select class (1=person, 2=suspicious_person, 3=thief, etc.)")
        print("  ENTER: Save annotations for current image")
        print("  N: Next image")
        print("  Q: Quit annotation")
        
        # Get all unannotated images
        image_files = list(self.images_dir.glob("*.jpg"))
        
        if not image_files:
            print("❌ No images found for annotation")
            return
        
        current_class = 0  # person
        class_names = self.annotations['metadata']['classes']
        
        for image_file in image_files:
            if self._is_image_annotated(image_file.name):
                continue
            
            print(f"📝 Annotating: {image_file.name}")
            
            # Load image
            image = cv2.imread(str(image_file))
            if image is None:
                continue
            
            # Annotation interface
            annotations = self._annotate_single_image(image, image_file.name, class_names)
            
            if annotations:
                self._save_image_annotations(image_file.name, annotations)
                print(f"✅ Saved annotations for {image_file.name}")
        
        self.save_annotations()
        print("✅ Interactive annotation completed")
    
    def _is_image_annotated(self, filename: str) -> bool:
        """Check if image is already annotated"""
        for category in ['theft_scenarios', 'suspicious_behaviors', 'normal_scenarios']:
            for item in self.annotations[category]:
                if item['filename'] == filename and item.get('objects'):
                    return True
        return False
    
    def _annotate_single_image(self, image: np.ndarray, filename: str, class_names: List[str]) -> List[Dict]:
        """Annotate a single image with bounding boxes"""
        annotations = []
        current_class = 0
        drawing = False
        start_point = None
        
        def mouse_callback(event, x, y, flags, param):
            nonlocal drawing, start_point, annotations
            
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                start_point = (x, y)
            
            elif event == cv2.EVENT_LBUTTONUP:
                if drawing and start_point:
                    end_point = (x, y)
                    
                    # Create bounding box annotation
                    x1, y1 = start_point
                    x2, y2 = end_point
                    
                    # Ensure proper order
                    x1, x2 = min(x1, x2), max(x1, x2)
                    y1, y2 = min(y1, y2), max(y1, y2)
                    
                    if x2 - x1 > 10 and y2 - y1 > 10:  # Minimum size
                        annotation = {
                            'class': class_names[current_class],
                            'class_id': current_class,
                            'bbox': [x1, y1, x2, y2],
                            'confidence': 1.0
                        }
                        annotations.append(annotation)
                        print(f"✅ Added {class_names[current_class]} at ({x1},{y1},{x2},{y2})")
                
                drawing = False
                start_point = None
        
        cv2.namedWindow('Annotation Tool')
        cv2.setMouseCallback('Annotation Tool', mouse_callback)
        
        while True:
            display_image = image.copy()
            
            # Draw existing annotations
            for ann in annotations:
                x1, y1, x2, y2 = ann['bbox']
                cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(display_image, ann['class'], (x1, y1-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Draw current class info
            cv2.putText(display_image, f"Class: {class_names[current_class]} (Press 1-{len(class_names)})", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(display_image, f"Objects: {len(annotations)}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.imshow('Annotation Tool', display_image)
            
            key = cv2.waitKey(1) & 0xFF
            
            # Class selection (1-7)
            if ord('1') <= key <= ord('7'):
                class_idx = key - ord('1')
                if class_idx < len(class_names):
                    current_class = class_idx
                    print(f"🎯 Selected class: {class_names[current_class]}")
            
            elif key == ord('\r') or key == ord('\n'):  # Enter - save
                cv2.destroyAllWindows()
                return annotations
            
            elif key == ord('n'):  # Next image
                cv2.destroyAllWindows()
                return annotations
            
            elif key == ord('q'):  # Quit
                cv2.destroyAllWindows()
                return None
        
        return annotations
    
    def _save_image_annotations(self, filename: str, annotations: List[Dict]):
        """Save annotations for a specific image"""
        # Find the image in annotations
        for category in ['theft_scenarios', 'suspicious_behaviors', 'normal_scenarios']:
            for item in self.annotations[category]:
                if item['filename'] == filename:
                    item['objects'] = annotations
                    break
    
    def create_yolo_dataset(self, train_split: float = 0.7, val_split: float = 0.2):
        """Create YOLO format dataset"""
        print("🔄 Creating YOLO format dataset...")
        
        # Collect all annotated images
        annotated_images = []
        
        for category in ['theft_scenarios', 'suspicious_behaviors', 'normal_scenarios']:
            for item in self.annotations[category]:
                if item.get('objects'):
                    annotated_images.append(item)
        
        if not annotated_images:
            print("❌ No annotated images found")
            return False
        
        # Shuffle and split
        np.random.shuffle(annotated_images)
        
        total_images = len(annotated_images)
        train_end = int(total_images * train_split)
        val_end = int(total_images * (train_split + val_split))
        
        train_images = annotated_images[:train_end]
        val_images = annotated_images[train_end:val_end]
        test_images = annotated_images[val_end:]
        
        # Create splits
        self._create_yolo_split(train_images, 'train')
        self._create_yolo_split(val_images, 'val')
        self._create_yolo_split(test_images, 'test')
        
        # Create dataset YAML
        self._create_dataset_yaml()
        
        print(f"✅ YOLO dataset created:")
        print(f"   Train: {len(train_images)} images")
        print(f"   Val: {len(val_images)} images")
        print(f"   Test: {len(test_images)} images")
        
        return True
    
    def _create_yolo_split(self, images: List[Dict], split: str):
        """Create YOLO format files for a dataset split"""
        split_img_dir = self.data_dir / split / "images"
        split_label_dir = self.data_dir / split / "labels"
        
        for image_data in images:
            filename = image_data['filename']
            
            # Copy image
            src_path = self.images_dir / filename
            dst_path = split_img_dir / filename
            
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                
                # Create YOLO format label
                label_filename = filename.replace('.jpg', '.txt')
                label_path = split_label_dir / label_filename
                
                with open(label_path, 'w') as f:
                    for obj in image_data['objects']:
                        # Convert to YOLO format (normalized)
                        x1, y1, x2, y2 = obj['bbox']
                        img_w, img_h = image_data['width'], image_data['height']
                        
                        # Calculate YOLO format: class_id center_x center_y width height
                        center_x = (x1 + x2) / 2 / img_w
                        center_y = (y1 + y2) / 2 / img_h
                        width = (x2 - x1) / img_w
                        height = (y2 - y1) / img_h
                        
                        f.write(f"{obj['class_id']} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")
    
    def _create_dataset_yaml(self):
        """Create YOLO dataset configuration file"""
        yaml_data = {
            'path': str(self.data_dir.absolute()),
            'train': 'train/images',
            'val': 'val/images',
            'test': 'test/images',
            'nc': len(self.annotations['metadata']['classes']),
            'names': self.annotations['metadata']['classes']
        }
        
        yaml_path = self.data_dir / 'dataset.yaml'
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_data, f, default_flow_style=False)
        
        print(f"✅ Created dataset.yaml at {yaml_path}")

class TheftModelTrainer:
    """Train custom models for theft detection"""
    
    def __init__(self, dataset_manager: TheftDatasetManager):
        self.dataset_manager = dataset_manager
        self.model_dir = Path("trained_models")
        self.model_dir.mkdir(exist_ok=True)
        
        print("🎯 Model trainer initialized")
    
    def train_yolo_model(self, epochs: int = 100, batch_size: int = 16, 
                        img_size: int = 640, model_size: str = 'n'):
        """
        Train custom YOLOv8 model for theft detection
        
        Args:
            epochs: Number of training epochs
            batch_size: Training batch size
            img_size: Input image size
            model_size: Model size ('n', 's', 'm', 'l', 'x')
        """
        print(f"🚀 Starting YOLOv8 model training...")
        
        # Check if dataset exists
        dataset_yaml = self.dataset_manager.data_dir / 'dataset.yaml'
        if not dataset_yaml.exists():
            print("❌ Dataset not found. Create dataset first.")
            return False
        
        try:
            # Load base model
            model = YOLO(f'yolov8{model_size}.pt')
            
            # Train the model
            results = model.train(
                data=str(dataset_yaml),
                epochs=epochs,
                batch=batch_size,
                imgsz=img_size,
                device='auto',  # Use GPU if available
                project=str(self.model_dir),
                name='theft_detection',
                exist_ok=True,
                save=True,
                save_period=10,  # Save checkpoint every 10 epochs
                val=True,
                plots=True,
                verbose=True
            )
            
            # Save model info
            model_info = {
                'model_type': 'YOLOv8',
                'model_size': model_size,
                'epochs': epochs,
                'batch_size': batch_size,
                'img_size': img_size,
                'trained_date': datetime.now().isoformat(),
                'dataset_path': str(dataset_yaml),
                'results': {
                    'best_model': str(results.save_dir / 'weights' / 'best.pt'),
                    'last_model': str(results.save_dir / 'weights' / 'last.pt')
                }
            }
            
            # Save model info
            info_path = self.model_dir / 'theft_detection' / 'model_info.json'
            with open(info_path, 'w') as f:
                json.dump(model_info, f, indent=2)
            
            print("✅ YOLOv8 training completed!")
            print(f"   Best model: {model_info['results']['best_model']}")
            print(f"   Last model: {model_info['results']['last_model']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def evaluate_model(self, model_path: str):
        """Evaluate trained model performance"""
        print(f"📊 Evaluating model: {model_path}")
        
        try:
            model = YOLO(model_path)
            
            # Run validation
            dataset_yaml = self.dataset_manager.data_dir / 'dataset.yaml'
            results = model.val(data=str(dataset_yaml))
            
            print("✅ Model evaluation completed!")
            print(f"   mAP50: {results.box.map50:.4f}")
            print(f"   mAP50-95: {results.box.map:.4f}")
            
            return results
            
        except Exception as e:
            print(f"❌ Evaluation failed: {e}")
            return None
    
    def test_model_real_time(self, model_path: str, camera_index: int = 0):
        """Test trained model in real-time"""
        print(f"🎥 Testing model in real-time: {model_path}")
        
        try:
            model = YOLO(model_path)
            cap = cv2.VideoCapture(camera_index)
            
            if not cap.isOpened():
                print(f"❌ Cannot open camera {camera_index}")
                return
            
            print("Press 'q' to quit real-time testing")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Run inference
                results = model(frame)
                
                # Draw results
                annotated_frame = results[0].plot()
                
                # Add performance info
                cv2.putText(annotated_frame, "Custom Theft Detection Model", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Real-time Theft Detection', annotated_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"❌ Real-time testing failed: {e}")

def main():
    """Main training interface"""
    print("🤖 Custom Theft Detection Model Trainer")
    print("=" * 50)
    
    # Initialize dataset manager
    dataset_manager = TheftDatasetManager()
    trainer = TheftModelTrainer(dataset_manager)
    
    while True:
        print("\nOptions:")
        print("1. Capture training data")
        print("2. Annotate images")
        print("3. Create YOLO dataset")
        print("4. Train custom model")
        print("5. Evaluate model")
        print("6. Test model real-time")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            scenario = input("Scenario type (normal/theft/suspicious): ").strip().lower()
            if scenario in ['normal', 'theft', 'suspicious']:
                dataset_manager.capture_training_data(scenario_type=scenario)
            else:
                print("❌ Invalid scenario type")
        
        elif choice == '2':
            dataset_manager.annotate_images_interactive()
        
        elif choice == '3':
            dataset_manager.create_yolo_dataset()
        
        elif choice == '4':
            epochs = int(input("Number of epochs (default 100): ") or 100)
            model_size = input("Model size n/s/m/l/x (default n): ").strip() or 'n'
            trainer.train_yolo_model(epochs=epochs, model_size=model_size)
        
        elif choice == '5':
            model_path = input("Model path: ").strip()
            if os.path.exists(model_path):
                trainer.evaluate_model(model_path)
            else:
                print("❌ Model file not found")
        
        elif choice == '6':
            model_path = input("Model path: ").strip()
            if os.path.exists(model_path):
                trainer.test_model_real_time(model_path)
            else:
                print("❌ Model file not found")
        
        elif choice == '7':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()