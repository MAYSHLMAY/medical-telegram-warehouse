from dagster import asset, Definitions, AssetIn
import subprocess
import os

# --- 1. Extraction Asset ---
@asset(group_name="ingestion")
def telegram_raw_data():
    """Runs the Telethon scraper to fetch JSON and Images."""
    # We call your existing script
    subprocess.run(["python", "src/scraper.py"], check=True)
    return "Data Scraped Successfully"

# --- 2. Load Asset ---
@asset(deps=[telegram_raw_data], group_name="ingestion")
def raw_postgres_table():
    """Loads raw JSON data into the PostgreSQL raw schema."""
    subprocess.run(["python", "src/database_loader.py"], check=True)
    return "Database Loaded"

# --- 3. Transformation Asset (dbt) ---
@asset(deps=[raw_postgres_table], group_name="transformation")
def dbt_medical_marts():
    """Triggers dbt run to build staging and fact tables."""
    # Change directory to your dbt project and run
    os.chdir("medical_warehouse")
    subprocess.run(["dbt", "run"], check=True)
    os.chdir("..")
    return "dbt Models Built"

# --- 4. AI Enrichment Asset ---
@asset(deps=[dbt_medical_marts], group_name="enrichment")
def yolo_detections():
    """Runs YOLOv8 object detection on scraped images."""
    subprocess.run(["python", "src/object_detector.py"], check=True)
    return "Objects Detected"

# --- 5. Final Linking Asset ---
@asset(deps=[yolo_detections], group_name="enrichment")
def refined_warehouse():
    """Links detection results back to the refined database layer."""
    subprocess.run(["python", "src/link_detections.py"], check=True)
    return "Warehouse Refined"

# --- Dagster Definitions ---
defs = Definitions(
    assets=[
        telegram_raw_data, 
        raw_postgres_table, 
        dbt_medical_marts, 
        yolo_detections, 
        refined_warehouse
    ]
)