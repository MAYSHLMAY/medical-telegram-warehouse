# Filename: link_detections.py
# Author: MAYSHLAMY
# Problem: Linking image detection results back to the database with schema protection

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def link_results():
    # 1. Establish connection to the medical warehouse
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    
    # 2. SCHEMA PROTECTION: Ensure columns exist in the refined table
    # This prevents the "UndefinedColumn" error if the table was recently replaced
    print("--- Checking Database Schema ---")
    cur.execute("""
        ALTER TABLE refined.medical_data 
        ADD COLUMN IF NOT EXISTS has_detection BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS detection_count INTEGER DEFAULT 0;
    """)
    conn.commit()

    # 3. Identify detected images
    detection_folder = 'data/detections'
    if not os.path.exists(detection_folder):
        print(f"❌ Error: Folder {detection_folder} not found!")
        return

    detected_files = [f for f in os.listdir(detection_folder) if f.startswith('detected_')]
    
    print(f"--- Linking {len(detected_files)} detections to Database ---")
    
    # 4. Link results using fuzzy matching on the image path
    for file_name in detected_files:
        # Extract the original filename (e.g., 'detected_9075.jpg' -> '9075.jpg')
        original_name = file_name.replace('detected_', '')
        
        query = """
            UPDATE refined.medical_data 
            SET has_detection = TRUE
            WHERE image_path LIKE %s
        """
        # We use % wrapping to match the filename within the full system path string
        cur.execute(query, (f"%{original_name}%",))
    
    conn.commit()
    print("✅ Database updated with AI detection flags!")
    
    # 5. Cleanup
    cur.close()
    conn.close()

if __name__ == '__main__':
    link_results()