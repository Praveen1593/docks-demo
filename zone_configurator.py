#!/usr/bin/env python3
"""
Interactive Zone Configuration Tool for Theft Detection
"""

import cv2
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple

class ZoneConfigurator:
    """Interactive tool for configuring theft detection zones"""
    
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.zones = {
            'restricted_zones': [],
            'valuable_zones': [],
            'entry_zones': [],
            'exit_zones': []
        }
        self.zone_file = Path("theft_zones.json")
        self.current_zone_type = 'restricted_zones'
        self.drawing = False
        self.start_point = None
        self.temp_rect = None
        
        # Load existing zones
        self.load_zones()
        
        print("🎯 Zone Configurator initialized")
        print("Available zone types:")
        print("  R - Restricted zones (unauthorized access)")
        print("  V - Valuable item zones (theft targets)")
        print("  E - Entry zones (monitoring entrances)")
        print("  X - Exit zones (monitoring exits)")
    
    def load_zones(self):
        """Load existing zone configuration"""
        if self.zone_file.exists():
            try:
                with open(self.zone_file, 'r') as f:
                    self.zones = json.load(f)
                print(f"✅ Loaded existing zones from {self.zone_file}")
            except Exception as e:
                print(f"⚠️ Error loading zones: {e}")
    
    def save_zones(self):
        """Save zone configuration to file"""
        try:
            with open(self.zone_file, 'w') as f:
                json.dump(self.zones, f, indent=2)
            print(f"💾 Zones saved to {self.zone_file}")
        except Exception as e:
            print(f"❌ Error saving zones: {e}")
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for zone drawing"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)
            self.temp_rect = None
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing and self.start_point:
                self.temp_rect = (self.start_point[0], self.start_point[1], x, y)
        
        elif event == cv2.EVENT_LBUTTONUP:
            if self.drawing and self.start_point:
                end_point = (x, y)
                self.add_zone(self.start_point, end_point)
                self.drawing = False
                self.start_point = None
                self.temp_rect = None
    
    def add_zone(self, start: Tuple[int, int], end: Tuple[int, int]):
        """Add a new zone"""
        x1, y1 = start
        x2, y2 = end
        
        # Ensure proper order
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        
        # Minimum size check
        if abs(x2 - x1) < 20 or abs(y2 - y1) < 20:
            print("⚠️ Zone too small, minimum size is 20x20 pixels")
            return
        
        # Get zone name
        zone_count = len(self.zones[self.current_zone_type]) + 1
        zone_name = input(f"\nEnter name for {self.current_zone_type[:-1]} #{zone_count}: ").strip()
        
        if not zone_name:
            zone_name = f"{self.current_zone_type[:-1]}_{zone_count}"
        
        # Create zone
        zone = {
            'name': zone_name,
            'type': self.current_zone_type,
            'bounds': [x1, y1, x2, y2],
            'enabled': True
        }
        
        self.zones[self.current_zone_type].append(zone)
        print(f"✅ Added {self.current_zone_type[:-1]}: {zone_name} at ({x1},{y1},{x2},{y2})")
    
    def draw_zones(self, frame: np.ndarray) -> np.ndarray:
        """Draw all zones on the frame"""
        display_frame = frame.copy()
        
        # Zone colors
        zone_colors = {
            'restricted_zones': (0, 0, 255),    # Red
            'valuable_zones': (0, 255, 255),    # Yellow
            'entry_zones': (0, 255, 0),         # Green
            'exit_zones': (255, 0, 0)           # Blue
        }
        
        # Draw existing zones
        for zone_type, zones in self.zones.items():
            color = zone_colors.get(zone_type, (255, 255, 255))
            
            for zone in zones:
                if not zone.get('enabled', True):
                    continue
                
                x1, y1, x2, y2 = zone['bounds']
                
                # Draw rectangle
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{zone['name']} ({zone_type[:-6]})"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                
                # Background for text
                cv2.rectangle(display_frame, 
                             (x1, y1 - label_size[1] - 10), 
                             (x1 + label_size[0], y1), 
                             color, -1)
                
                # Text
                cv2.putText(display_frame, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw temporary rectangle while drawing
        if self.temp_rect:
            x1, y1, x2, y2 = self.temp_rect
            color = zone_colors.get(self.current_zone_type, (255, 255, 255))
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
        
        return display_frame
    
    def add_zone_info(self, frame: np.ndarray) -> np.ndarray:
        """Add zone configuration info to frame"""
        h, w = frame.shape[:2]
        
        # Current zone type
        cv2.putText(frame, f"Current Zone: {self.current_zone_type[:-6].upper()}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        # Instructions
        instructions = [
            "Controls:",
            "R - Restricted zones",
            "V - Valuable zones",
            "E - Entry zones",
            "X - Exit zones",
            "D - Delete last zone",
            "C - Clear all zones",
            "S - Save zones",
            "Q - Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            y = h - (len(instructions) - i) * 25
            cv2.putText(frame, instruction, (10, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Zone counts
        zone_counts = []
        for zone_type, zones in self.zones.items():
            enabled_count = sum(1 for z in zones if z.get('enabled', True))
            zone_counts.append(f"{zone_type[:-6]}: {enabled_count}")
        
        for i, count in enumerate(zone_counts):
            cv2.putText(frame, count, (w - 200, 30 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def delete_last_zone(self):
        """Delete the last added zone of current type"""
        if self.zones[self.current_zone_type]:
            deleted = self.zones[self.current_zone_type].pop()
            print(f"🗑️ Deleted zone: {deleted['name']}")
        else:
            print("⚠️ No zones to delete for current type")
    
    def clear_all_zones(self):
        """Clear all zones of current type"""
        count = len(self.zones[self.current_zone_type])
        if count > 0:
            response = input(f"Are you sure you want to delete all {count} {self.current_zone_type}? (y/N): ")
            if response.lower() == 'y':
                self.zones[self.current_zone_type] = []
                print(f"🗑️ Cleared all {self.current_zone_type}")
        else:
            print(f"⚠️ No {self.current_zone_type} to clear")
    
    def configure_zones(self):
        """Main zone configuration interface"""
        print("\n🎯 Starting Zone Configuration")
        print("Draw rectangles by clicking and dragging")
        print("Use keyboard shortcuts to change zone types")
        
        cap = cv2.VideoCapture(self.camera_index)
        
        if not cap.isOpened():
            print(f"❌ Cannot open camera {self.camera_index}")
            return
        
        cv2.namedWindow('Zone Configuration', cv2.WINDOW_RESIZABLE)
        cv2.setMouseCallback('Zone Configuration', self.mouse_callback)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            # Draw zones
            display_frame = self.draw_zones(frame)
            
            # Add info overlay
            display_frame = self.add_zone_info(display_frame)
            
            cv2.imshow('Zone Configuration', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):  # Quit
                break
            elif key == ord('r'):  # Restricted zones
                self.current_zone_type = 'restricted_zones'
                print("🔴 Switched to Restricted Zones")
            elif key == ord('v'):  # Valuable zones
                self.current_zone_type = 'valuable_zones'
                print("🟡 Switched to Valuable Zones")
            elif key == ord('e'):  # Entry zones
                self.current_zone_type = 'entry_zones'
                print("🟢 Switched to Entry Zones")
            elif key == ord('x'):  # Exit zones
                self.current_zone_type = 'exit_zones'
                print("🔵 Switched to Exit Zones")
            elif key == ord('d'):  # Delete last zone
                self.delete_last_zone()
            elif key == ord('c'):  # Clear all zones
                self.clear_all_zones()
            elif key == ord('s'):  # Save zones
                self.save_zones()
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Final save
        self.save_zones()
        
        # Summary
        self.print_zone_summary()
    
    def print_zone_summary(self):
        """Print zone configuration summary"""
        print("\n📊 Zone Configuration Summary")
        print("=" * 40)
        
        total_zones = 0
        for zone_type, zones in self.zones.items():
            enabled_zones = [z for z in zones if z.get('enabled', True)]
            total_zones += len(enabled_zones)
            
            if enabled_zones:
                print(f"\n{zone_type.replace('_', ' ').title()}:")
                for zone in enabled_zones:
                    x1, y1, x2, y2 = zone['bounds']
                    print(f"  - {zone['name']}: ({x1},{y1}) to ({x2},{y2})")
        
        print(f"\nTotal Zones: {total_zones}")
        print(f"Configuration saved to: {self.zone_file}")
    
    def export_zones_for_monitor(self, output_file: str = "monitor_zones.py"):
        """Export zones as Python code for the AI monitor"""
        try:
            with open(output_file, 'w') as f:
                f.write("#!/usr/bin/env python3\n")
                f.write('"""\nAuto-generated zone configuration for AI Monitor\n"""\n\n')
                f.write("def setup_theft_zones(theft_detector):\n")
                f.write('    """Setup theft detection zones"""\n')
                
                # Restricted zones
                if self.zones['restricted_zones']:
                    f.write('\n    # Restricted Zones\n')
                    for zone in self.zones['restricted_zones']:
                        if zone.get('enabled', True):
                            bounds = tuple(zone['bounds'])
                            f.write(f'    theft_detector.add_restricted_zone("{zone["name"]}", {bounds})\n')
                
                # Valuable zones
                if self.zones['valuable_zones']:
                    f.write('\n    # Valuable Item Zones\n')
                    for zone in self.zones['valuable_zones']:
                        if zone.get('enabled', True):
                            bounds = tuple(zone['bounds'])
                            f.write(f'    theft_detector.add_valuable_item_zone("{zone["name"]}", {bounds})\n')
                
                f.write('\n    print("✅ Theft detection zones configured")\n')
            
            print(f"✅ Zones exported to {output_file}")
            print("To use in AI monitor, import and call setup_theft_zones(theft_detector)")
            
        except Exception as e:
            print(f"❌ Error exporting zones: {e}")

def main():
    """Main zone configuration function"""
    print("🎯 Theft Detection Zone Configurator")
    print("=" * 50)
    
    configurator = ZoneConfigurator()
    
    while True:
        print("\nOptions:")
        print("1. Configure zones interactively")
        print("2. View current zones")
        print("3. Export zones for AI monitor")
        print("4. Clear all zones")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            configurator.configure_zones()
        
        elif choice == '2':
            configurator.print_zone_summary()
        
        elif choice == '3':
            output_file = input("Output file name (default: monitor_zones.py): ").strip()
            if not output_file:
                output_file = "monitor_zones.py"
            configurator.export_zones_for_monitor(output_file)
        
        elif choice == '4':
            confirm = input("Are you sure you want to clear ALL zones? (y/N): ").strip().lower()
            if confirm == 'y':
                configurator.zones = {
                    'restricted_zones': [],
                    'valuable_zones': [],
                    'entry_zones': [],
                    'exit_zones': []
                }
                configurator.save_zones()
                print("🗑️ All zones cleared")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()