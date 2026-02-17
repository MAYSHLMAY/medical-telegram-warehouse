# Filename: main.py
# Author: MAYSHLAMY
# Problem: Task 6 - Robust FastAPI for Medical Data Warehouse

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MAYSHLAMY Medical Data API")

# Database Connection
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Data Warehouse API"}

@app.get("/detections")
def get_all_medical_data():
    """Fetches all cleaned medical records from the refined layer."""
    try:
        query = "SELECT * FROM refined.medical_data"
        df = pd.read_sql(query, engine)
        
        # Clean data for JSON compliance
        df['image_path'] = df['image_path'].replace({0: "None", "0": "None"})
        df = df.fillna(0)
        
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/{keyword}")
def search_medical_data(keyword: str):
    """Search for specific medical terms using safe parameterized queries."""
    try:
        # Using sqlalchemy.text to prevent SQL Injection
        query = text("SELECT * FROM refined.medical_data WHERE cleaned_content ILIKE :key")
        df = pd.read_sql(query, engine, params={"key": f"%{keyword}%"})
        
        if df.empty:
            return {"message": f"No records found for: {keyword}"}
        
        # Replace image_path 0 with "None" and handle NaNs for JSON compliance
        df['image_path'] = df['image_path'].replace({0: "None", "0": "None"})
        df = df.fillna(0) 
            
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/detections/confirmed")
def get_confirmed_detections():
    """Returns only records where YOLO detected medical objects."""
    try:
        query = "SELECT * FROM refined.medical_data WHERE has_detection = TRUE"
        df = pd.read_sql(query, engine)
        
        # Standard cleaning
        df['image_path'] = df['image_path'].replace({0: "None", "0": "None"})
        df = df.fillna(0)
        
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)