#!/usr/bin/env python3
"""
Advanced Theft Detection System
Combines object detection, motion analysis, and behavioral patterns
"""

import cv2
import numpy as np
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from ultralytics import YOLO
import mediapipe as mp
from collections import deque

class TheftDetector:
    """Advanced theft detection using multiple AI techniques"""
    
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """Initialize the theft detector"""
        self.model = YOLO(model_path)
        
        # Motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.motion_history = deque(maxlen=30)  # Last 30 frames
        
        # Person tracking
        self.tracker = cv2.TrackerCSRT_create()
        self.tracked_objects = {}
        self.next_id = 0
        
        # Mediapipe for pose detection
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5
        )
        
        # Theft-specific object classes
        self.theft_objects = {
            'bag', 'backpack', 'handbag', 'suitcase', 'laptop', 
            'cell phone', 'wallet', 'purse', 'briefcase', 'camera',
            'tablet', 'jewelry', 'watch', 'keys', 'bicycle',
            'motorcycle', 'car', 'truck'
        }
        
        # Suspicious behavior patterns
        self.behavior_history = {}
        self.theft_confidence_threshold = 0.7
        
        # Zone definitions (can be customized)
        self.restricted_zones = []
        self.valuable_item_zones = []
        
        print("🔍 Advanced Theft Detector initialized")
    
    def detect_theft_scenario(self, frame: np.ndarray, frame_id: int) -> Dict:
        """
        Main theft detection function
        
        Args:
            frame: Input frame from camera
            frame_id: Frame number for tracking
            
        Returns:
            Dictionary with theft detection results
        """
        results = {
            'theft_detected': False,
            'confidence': 0.0,
            'theft_type': None,
            'suspicious_persons': [],
            'stolen_objects': [],
            'suspicious_behaviors': [],
            'motion_level': 0.0,
            'alert_level': 'LOW'  # LOW, MEDIUM, HIGH, CRITICAL
        }
        
        # 1. Object Detection
        objects = self._detect_objects(frame)
        
        # 2. Motion Analysis
        motion_level = self._analyze_motion(frame)
        results['motion_level'] = motion_level
        
        # 3. Person Detection and Tracking
        persons = self._detect_and_track_persons(frame, objects, frame_id)
        
        # 4. Pose Analysis for Suspicious Behavior
        suspicious_behaviors = self._analyze_suspicious_behavior(frame, persons)
        results['suspicious_behaviors'] = suspicious_behaviors
        
        # 5. Object Disappearance Detection
        missing_objects = self._detect_missing_objects(objects, frame_id)
        
        # 6. Zone Violation Detection
        zone_violations = self._detect_zone_violations(persons, objects)
        
        # 7. Behavior Pattern Analysis
        behavior_analysis = self._analyze_behavior_patterns(persons, frame_id)
        
        # 8. Combine all factors for theft detection
        theft_analysis = self._evaluate_theft_probability(
            motion_level, suspicious_behaviors, missing_objects,
            zone_violations, behavior_analysis, persons, objects
        )
        
        results.update(theft_analysis)
        
        return results
    
    def _detect_objects(self, frame: np.ndarray) -> List[Dict]:
        """Detect objects in frame"""
        objects = []
        
        try:
            results = self.model(frame, verbose=False)
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[class_id]
                        
                        if confidence >= 0.5:
                            objects.append({
                                'class_name': class_name,
                                'confidence': float(confidence),
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'center': [(x1+x2)/2, (y1+y2)/2],
                                'area': (x2-x1) * (y2-y1),
                                'is_valuable': class_name.lower() in self.theft_objects
                            })
        except Exception as e:
            print(f"⚠️ Object detection error: {e}")
        
        return objects
    
    def _analyze_motion(self, frame: np.ndarray) -> float:
        """Analyze motion level in frame"""
        try:
            # Background subtraction
            fg_mask = self.bg_subtractor.apply(frame)
            
            # Calculate motion percentage
            motion_pixels = cv2.countNonZero(fg_mask)
            total_pixels = fg_mask.shape[0] * fg_mask.shape[1]
            motion_percentage = motion_pixels / total_pixels
            
            # Store motion history
            self.motion_history.append(motion_percentage)
            
            # Calculate average motion over time
            avg_motion = np.mean(self.motion_history) if self.motion_history else 0
            
            return float(avg_motion)
            
        except Exception as e:
            print(f"⚠️ Motion analysis error: {e}")
            return 0.0
    
    def _detect_and_track_persons(self, frame: np.ndarray, objects: List[Dict], frame_id: int) -> List[Dict]:
        """Detect and track persons with behavioral analysis"""
        persons = []
        
        # Extract person objects
        person_objects = [obj for obj in objects if obj['class_name'] == 'person']
        
        for person_obj in person_objects:
            person_data = person_obj.copy()
            
            # Add tracking information
            person_id = self._get_or_create_person_id(person_obj, frame_id)
            person_data['person_id'] = person_id
            
            # Analyze person's pose
            pose_analysis = self._analyze_person_pose(frame, person_obj['bbox'])
            person_data.update(pose_analysis)
            
            # Calculate movement patterns
            movement_data = self._analyze_person_movement(person_id, person_obj['center'], frame_id)
            person_data.update(movement_data)
            
            persons.append(person_data)
        
        return persons
    
    def _get_or_create_person_id(self, person_obj: Dict, frame_id: int) -> int:
        """Assign unique ID to tracked person"""
        person_center = person_obj['center']
        
        # Find closest existing tracked person
        min_distance = float('inf')
        closest_id = None
        
        for pid, data in self.tracked_objects.items():
            if 'last_center' in data:
                distance = np.sqrt(
                    (person_center[0] - data['last_center'][0])**2 + 
                    (person_center[1] - data['last_center'][1])**2
                )
                if distance < min_distance and distance < 100:  # 100 pixel threshold
                    min_distance = distance
                    closest_id = pid
        
        if closest_id is not None:
            # Update existing track
            self.tracked_objects[closest_id]['last_center'] = person_center
            self.tracked_objects[closest_id]['last_seen'] = frame_id
            return closest_id
        else:
            # Create new track
            person_id = self.next_id
            self.next_id += 1
            self.tracked_objects[person_id] = {
                'first_seen': frame_id,
                'last_seen': frame_id,
                'last_center': person_center,
                'movement_history': [person_center],
                'behavior_score': 0.0
            }
            return person_id
    
    def _analyze_person_pose(self, frame: np.ndarray, bbox: List[int]) -> Dict:
        """Analyze person's pose for suspicious behavior"""
        pose_data = {
            'pose_confidence': 0.0,
            'is_crouching': False,
            'is_reaching': False,
            'head_direction': 'unknown',
            'body_posture': 'normal'
        }
        
        try:
            # Extract person region
            x1, y1, x2, y2 = bbox
            person_roi = frame[y1:y2, x1:x2]
            
            if person_roi.size > 0:
                # Convert to RGB for mediapipe
                rgb_roi = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)
                
                # Pose detection
                results = self.pose.process(rgb_roi)
                
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Analyze pose characteristics
                    pose_data['pose_confidence'] = 0.8  # Simplified
                    
                    # Check for crouching (knees bent, lower body position)
                    left_knee = landmarks[25]
                    right_knee = landmarks[26]
                    left_hip = landmarks[23]
                    right_hip = landmarks[24]
                    
                    if left_knee.y > left_hip.y and right_knee.y > right_hip.y:
                        pose_data['is_crouching'] = True
                        pose_data['body_posture'] = 'crouching'
                    
                    # Check for reaching behavior
                    left_wrist = landmarks[15]
                    right_wrist = landmarks[16]
                    nose = landmarks[0]
                    
                    if (abs(left_wrist.x - nose.x) > 0.3 or 
                        abs(right_wrist.x - nose.x) > 0.3):
                        pose_data['is_reaching'] = True
                    
        except Exception as e:
            print(f"⚠️ Pose analysis error: {e}")
        
        return pose_data
    
    def _analyze_person_movement(self, person_id: int, current_center: Tuple[float, float], frame_id: int) -> Dict:
        """Analyze movement patterns"""
        movement_data = {
            'speed': 0.0,
            'direction_change': 0.0,
            'loitering_time': 0.0,
            'erratic_movement': False
        }
        
        if person_id in self.tracked_objects:
            track_data = self.tracked_objects[person_id]
            history = track_data.get('movement_history', [])
            
            # Add current position to history
            history.append(current_center)
            if len(history) > 20:  # Keep last 20 positions
                history.pop(0)
            track_data['movement_history'] = history
            
            if len(history) >= 2:
                # Calculate speed
                prev_center = history[-2]
                distance = np.sqrt(
                    (current_center[0] - prev_center[0])**2 + 
                    (current_center[1] - prev_center[1])**2
                )
                movement_data['speed'] = distance
                
                # Calculate direction changes
                if len(history) >= 3:
                    direction_changes = 0
                    for i in range(2, len(history)):
                        vec1 = np.array(history[i-1]) - np.array(history[i-2])
                        vec2 = np.array(history[i]) - np.array(history[i-1])
                        
                        if np.linalg.norm(vec1) > 0 and np.linalg.norm(vec2) > 0:
                            angle = np.arccos(np.clip(np.dot(vec1, vec2) / 
                                                    (np.linalg.norm(vec1) * np.linalg.norm(vec2)), -1, 1))
                            if angle > np.pi/3:  # 60 degrees
                                direction_changes += 1
                    
                    movement_data['direction_change'] = direction_changes / len(history)
                    movement_data['erratic_movement'] = direction_changes > len(history) * 0.3
                
                # Calculate loitering time
                if movement_data['speed'] < 5:  # Very slow movement
                    movement_data['loitering_time'] = frame_id - track_data['first_seen']
        
        return movement_data
    
    def _analyze_suspicious_behavior(self, frame: np.ndarray, persons: List[Dict]) -> List[Dict]:
        """Analyze suspicious behaviors"""
        suspicious_behaviors = []
        
        for person in persons:
            suspicion_score = 0.0
            behaviors = []
            
            # Check for crouching near valuable items
            if person.get('is_crouching'):
                suspicion_score += 0.3
                behaviors.append('crouching_behavior')
            
            # Check for reaching movements
            if person.get('is_reaching'):
                suspicion_score += 0.2
                behaviors.append('reaching_behavior')
            
            # Check for erratic movement
            if person.get('erratic_movement'):
                suspicion_score += 0.4
                behaviors.append('erratic_movement')
            
            # Check for loitering
            if person.get('loitering_time', 0) > 100:  # 100 frames
                suspicion_score += 0.3
                behaviors.append('loitering')
            
            # Check for fast movement (possible escape)
            if person.get('speed', 0) > 20:
                suspicion_score += 0.5
                behaviors.append('rapid_movement')
            
            if suspicion_score > 0.4:  # Threshold for suspicious behavior
                suspicious_behaviors.append({
                    'person_id': person['person_id'],
                    'suspicion_score': suspicion_score,
                    'behaviors': behaviors,
                    'bbox': person['bbox']
                })
        
        return suspicious_behaviors
    
    def _detect_missing_objects(self, current_objects: List[Dict], frame_id: int) -> List[Dict]:
        """Detect if valuable objects have disappeared"""
        # This would require object tracking across frames
        # Simplified implementation
        missing_objects = []
        
        # Store current valuable objects
        current_valuables = [obj for obj in current_objects if obj['is_valuable']]
        
        # Compare with previous frame (simplified)
        # In a full implementation, this would track objects across frames
        
        return missing_objects
    
    def _detect_zone_violations(self, persons: List[Dict], objects: List[Dict]) -> List[Dict]:
        """Detect violations of restricted zones"""
        violations = []
        
        # Check if persons are in restricted zones
        for person in persons:
            person_center = person['center']
            
            for zone in self.restricted_zones:
                if self._point_in_zone(person_center, zone):
                    violations.append({
                        'type': 'person_in_restricted_zone',
                        'person_id': person['person_id'],
                        'zone': zone,
                        'severity': 'HIGH'
                    })
        
        return violations
    
    def _point_in_zone(self, point: Tuple[float, float], zone: Dict) -> bool:
        """Check if point is inside a defined zone"""
        # Simplified rectangular zone check
        x, y = point
        if 'bounds' in zone:
            x1, y1, x2, y2 = zone['bounds']
            return x1 <= x <= x2 and y1 <= y <= y2
        return False
    
    def _analyze_behavior_patterns(self, persons: List[Dict], frame_id: int) -> Dict:
        """Analyze long-term behavior patterns"""
        analysis = {
            'suspicious_patterns': [],
            'confidence': 0.0
        }
        
        for person in persons:
            person_id = person['person_id']
            
            if person_id in self.behavior_history:
                # Analyze historical behavior
                history = self.behavior_history[person_id]
                
                # Look for patterns that indicate theft
                if len(history) > 50:  # Enough history
                    # Calculate behavior consistency
                    recent_behaviors = history[-20:]
                    if any('suspicious' in str(b) for b in recent_behaviors):
                        analysis['suspicious_patterns'].append({
                            'person_id': person_id,
                            'pattern': 'consistent_suspicious_behavior'
                        })
                        analysis['confidence'] += 0.4
            else:
                self.behavior_history[person_id] = []
            
            # Add current behavior to history
            current_behavior = {
                'frame': frame_id,
                'speed': person.get('speed', 0),
                'suspicious_score': sum([
                    0.3 if person.get('is_crouching') else 0,
                    0.2 if person.get('is_reaching') else 0,
                    0.4 if person.get('erratic_movement') else 0
                ])
            }
            self.behavior_history[person_id].append(current_behavior)
            
            # Keep only recent history
            if len(self.behavior_history[person_id]) > 100:
                self.behavior_history[person_id].pop(0)
        
        return analysis
    
    def _evaluate_theft_probability(self, motion_level: float, suspicious_behaviors: List[Dict],
                                  missing_objects: List[Dict], zone_violations: List[Dict],
                                  behavior_analysis: Dict, persons: List[Dict], 
                                  objects: List[Dict]) -> Dict:
        """Evaluate overall theft probability"""
        
        theft_confidence = 0.0
        theft_factors = []
        alert_level = 'LOW'
        
        # Motion factor
        if motion_level > 0.15:
            theft_confidence += 0.2
            theft_factors.append('high_motion')
        
        # Suspicious behavior factor
        if suspicious_behaviors:
            behavior_score = max([b['suspicion_score'] for b in suspicious_behaviors])
            theft_confidence += behavior_score * 0.6
            theft_factors.append('suspicious_behavior')
        
        # Missing objects factor
        if missing_objects:
            theft_confidence += 0.8
            theft_factors.append('missing_objects')
        
        # Zone violations factor
        if zone_violations:
            theft_confidence += 0.5
            theft_factors.append('zone_violation')
        
        # Behavior pattern factor
        if behavior_analysis['suspicious_patterns']:
            theft_confidence += behavior_analysis['confidence']
            theft_factors.append('suspicious_patterns')
        
        # Multiple persons factor (organized theft)
        if len(persons) > 2:
            theft_confidence += 0.2
            theft_factors.append('multiple_suspects')
        
        # Valuable objects present factor
        valuable_objects = [obj for obj in objects if obj['is_valuable']]
        if valuable_objects and suspicious_behaviors:
            theft_confidence += 0.3
            theft_factors.append('valuables_at_risk')
        
        # Determine alert level
        if theft_confidence >= 0.8:
            alert_level = 'CRITICAL'
        elif theft_confidence >= 0.6:
            alert_level = 'HIGH'
        elif theft_confidence >= 0.4:
            alert_level = 'MEDIUM'
        
        # Determine theft detection
        theft_detected = theft_confidence >= self.theft_confidence_threshold
        
        return {
            'theft_detected': theft_detected,
            'confidence': min(theft_confidence, 1.0),
            'theft_factors': theft_factors,
            'alert_level': alert_level,
            'suspicious_persons': suspicious_behaviors,
            'stolen_objects': missing_objects,
            'theft_type': self._classify_theft_type(theft_factors)
        }
    
    def _classify_theft_type(self, factors: List[str]) -> Optional[str]:
        """Classify the type of theft based on factors"""
        if 'missing_objects' in factors:
            return 'OBJECT_THEFT'
        elif 'zone_violation' in factors:
            return 'UNAUTHORIZED_ACCESS'
        elif 'multiple_suspects' in factors:
            return 'ORGANIZED_THEFT'
        elif 'suspicious_behavior' in factors:
            return 'SUSPICIOUS_ACTIVITY'
        else:
            return 'POTENTIAL_THEFT'
    
    def add_restricted_zone(self, zone_name: str, bounds: Tuple[int, int, int, int]):
        """Add a restricted zone for monitoring"""
        self.restricted_zones.append({
            'name': zone_name,
            'bounds': bounds  # (x1, y1, x2, y2)
        })
        print(f"✅ Added restricted zone: {zone_name}")
    
    def add_valuable_item_zone(self, zone_name: str, bounds: Tuple[int, int, int, int]):
        """Add a zone where valuable items are located"""
        self.valuable_item_zones.append({
            'name': zone_name,
            'bounds': bounds  # (x1, y1, x2, y2)
        })
        print(f"✅ Added valuable item zone: {zone_name}")
    
    def draw_theft_annotations(self, frame: np.ndarray, theft_results: Dict) -> np.ndarray:
        """Draw theft detection annotations on frame"""
        annotated_frame = frame.copy()
        
        # Draw alert level indicator
        alert_level = theft_results['alert_level']
        alert_colors = {
            'LOW': (0, 255, 0),      # Green
            'MEDIUM': (0, 255, 255), # Yellow
            'HIGH': (0, 165, 255),   # Orange
            'CRITICAL': (0, 0, 255)  # Red
        }
        
        color = alert_colors.get(alert_level, (255, 255, 255))
        
        # Draw alert banner
        cv2.rectangle(annotated_frame, (10, 10), (300, 80), color, -1)
        cv2.putText(annotated_frame, f"THEFT ALERT: {alert_level}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(annotated_frame, f"Confidence: {theft_results['confidence']:.2f}", (20, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        # Draw suspicious persons
        for person in theft_results['suspicious_persons']:
            x1, y1, x2, y2 = person['bbox']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(annotated_frame, f"SUSPECT ID:{person['person_id']}", 
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw restricted zones
        for zone in self.restricted_zones:
            if 'bounds' in zone:
                x1, y1, x2, y2 = zone['bounds']
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(annotated_frame, f"RESTRICTED: {zone['name']}", 
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Draw valuable item zones
        for zone in self.valuable_item_zones:
            if 'bounds' in zone:
                x1, y1, x2, y2 = zone['bounds']
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.putText(annotated_frame, f"VALUABLE: {zone['name']}", 
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return annotated_frame