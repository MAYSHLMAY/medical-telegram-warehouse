# Filename: data_cleaner.py
# Author: MAYSHLAMY
# Problem: Task 3 - Final Medical Refinement for Multi-language Data

import pandas as pd
import re
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

class MedicalDataCleaner:
    def __init__(self):
        # Using SQLAlchemy for database connection
        self.db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.engine = create_engine(self.db_url)

    def load_data(self):
        query = "SELECT * FROM staging.fact_medical_messages"
        return pd.read_sql(query, self.engine)

    def clean_text(self, text):
        if not text:
            return ""
        
        # 1. Block Russian/Cyrillic entirely
        if re.search(r'[\u0400-\u04FF]', text):
            return "FILTERED_NOISE"

        # 2. Kill Football, Holiday, and Travel Noise
        # Patterns found in your specific data sample
        noise_patterns = [
            'منتخبنا', 'فوزه', 'كأس العالم', 'አዲስ ዓመት', 'እንኳን አደረሳችሁ', 
            'መልካም በዓል', 'мексика', 'сомбреро', 'travel', 'vlog', 't.me'
        ]
        if any(pattern in text for pattern in noise_patterns):
            return "FILTERED_NOISE"

        # 3. Medical Relevance Check (English, Amharic, Arabic)
        medical_keywords = [
        # English
        'anemia', 'sarcoidosis', 'mri', 'pediatrics', 'urology', 'pharmacology', 
        'syndrome', 'patient', 'guidelines', 'hospital', 'medication', 'dose',
        # Amharic (Medical & Health)
        'መድሃኒት', 'ጤና', 'ሐኪም', 'ቫይረስ', 'ምርመራ', 'ህክምና', 'ኢንሱሊን', 'ቆሽት',
        # Arabic (Medical)
        'صيدلة', 'طبية', 'علاج', 'أدوية', 'كيس', 'تشخيص', 'فحص'
        ]
        
        text_lower = text.lower()
        has_medical_term = any(med in text_lower for med in medical_keywords)
        
        # If no medical keywords are found and the message is short, it's junk
        if not has_medical_term and len(text.split()) < 15:
            return "FILTERED_NOISE"

        # 4. Standard Cleaning (URLs and Whitespace)
        text = re.sub(r'http\S+|www\S+|https\S+|@\w+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def save_data(self, df):
        print("--- Saving cleaned data to refined.medical_data ---")
        # Overwrite with the professional, noise-free version
        df.to_sql('medical_data', self.engine, schema='refined', if_exists='replace', index=False)
        print("✅ Data successfully saved to refined.medical_data!")

    def run_pipeline(self):
        print("--- Loading data from Warehouse ---")
        df = self.load_data()
        
        print("--- Cleaning text and applying Medical Filters ---")
        df['cleaned_content'] = df['content'].apply(self.clean_text)
        
        # REMOVE the noise rows so they don't appear in our final table
        initial_count = len(df)
        df = df[df['cleaned_content'] != "FILTERED_NOISE"]
        final_count = len(df)
        
        print(f"--- Filtered out {initial_count - final_count} noise/ad messages ---")
        print(f"--- Final medical record count: {final_count} ---")
        
        print("\nSample of Cleaned Data:")
        print(df[['content', 'cleaned_content']].head())
        
        self.save_data(df)
        return df

if __name__ == "__main__":
    cleaner = MedicalDataCleaner()
    cleaned_df = cleaner.run_pipeline()