# Filename: database_loader.py
# Author: MAYSHLAMY
# Problem: Loading scraped JSON data into PostgreSQL Raw Schema

import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

def load_json_to_postgres():
    base_path = 'data/raw/telegram_messages'
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("--- Starting Data Load to PostgreSQL ---")
    
    # Iterate through date folders (e.g., 2026-02-17)
    for date_folder in os.listdir(base_path):
        date_path = os.path.join(base_path, date_folder)
        
        if os.path.isdir(date_path):
            # Iterate through JSON files in each date folder
            for json_file in os.listdir(date_path):
                if json_file.endswith('.json'):
                    file_path = os.path.join(date_path, json_file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            messages = json.load(f)
                            for msg in messages:
                                # Prepare the SQL Insert
                                insert_query = """
                                INSERT INTO raw.telegram_messages 
                                (channel_name, message_id, message_date, message_text, has_media, views, forwards, image_path)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                """
                                values = (
                                    msg['channel_name'],
                                    msg['message_id'],
                                    msg['message_date'],
                                    msg['message_text'],
                                    msg['has_media'],
                                    msg['views'],
                                    msg['forwards'],
                                    msg['image_path']
                                )
                                cur.execute(insert_query, values)
                            
                            print(f"✅ Loaded {len(messages)} messages from {json_file}")
                        except Exception as e:
                            print(f"❌ Error loading {json_file}: {e}")
 
    conn.commit()
    cur.close()
    conn.close()
    print("--- All data successfully loaded! ---")

if __name__ == "__main__":
    load_json_to_postgres()