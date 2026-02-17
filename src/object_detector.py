# Filename: object_detector.py
# Author: MAYSHLAMY
# Problem: Task 4 - Object Detection on Scraped Medical Images

import os
import cv2
from ultralytics import YOLO

class MedicalObjectDetector:
    def __init__(self, model_name='yolov8n.pt'):
        print(f"--- Loading Model: {model_name} ---")
        self.model = YOLO(model_name)

# Updated detection loop inside src/object_detector.py

    def detect_in_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    img_path = os.path.join(root, file)
                    
                    # Check if file is empty before processing
                    if os.path.getsize(img_path) == 0:
                        print(f"⚠️ Skipping empty file: {file}")
                        continue

                    try:
                        print(f"Processing: {file}")
                        results = self.model(img_path)
                        
                        for result in results:
                            # Only save if we actually found something
                            if len(result.boxes) > 0:
                                result.save(filename=f"detected_{file}")
                                for box in result.boxes:
                                    label = self.model.names[int(box.cls[0])]
                                    print(f"  - Found: {label} ({float(box.conf[0]):.2f})")
                            else:
                                print(f"  - No objects detected in {file}")
                                
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")
                        continue # Keep going even if one image fails

if __name__ == "__main__":
    detector = MedicalObjectDetector()
    # Point this to your actual image folder
    image_dir = 'data/raw/images'
    detector.detect_in_folder(image_dir)