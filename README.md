# 🏥 Medical Telegram Data Warehouse
## From Raw Telegram Data to an Analytical API

**Author:** Mikiyas Dawit Abera  
**Project Type:** Data Engineering & AI Integration  
**Tech Stack:** Python, PostgreSQL, dbt, Dagster, FastAPI, YOLOv8, Playwright

---

## 📌 Project Overview

This project implements an end-to-end data engineering pipeline that extracts medical and pharmaceutical information from public Ethiopian Telegram channels, transforms and enriches the data, and exposes it through a production-ready analytical API.

The system is designed to support analytical questions around:
- medical product visibility and availability,
- public health updates (e.g., outbreak-related posts),
- visual content usage across Telegram channels,
- keyword-based medical trend analysis.

The final output is a clean, structured PostgreSQL data warehouse served through FastAPI.

---

## 🏗️ System Architecture

The pipeline follows a modern ELT architecture:

1. **Ingestion**  
   Telegram messages and images are scraped from public channels and stored in a raw data lake.

2. **Loading & Transformation (dbt)**  
   Raw JSON data is loaded into PostgreSQL and transformed into a dimensional star schema using dbt.

3. **Data Enrichment (Computer Vision)**  
   YOLOv8 is used to detect objects in images and classify visual content.

4. **Serving Layer**  
   A FastAPI application exposes analytical endpoints for downstream consumption.

---

## 🧠 Key Features

- Multilingual support (Amharic & English)
- Structured data warehouse with dbt testing
- AI-powered image enrichment using YOLOv8
- Secure, parameterized database queries
- Fully documented REST API (Swagger / OpenAPI)
- Pipeline orchestration and observability with Dagster

---

## 🚀 API Capabilities

The API is automatically documented and accessible via Swagger UI.

### 1. Global Medical Records
Returns all cleaned and processed medical messages.

![All Medical Records](./assets/api_all_data.png)

---

### 2. YOLO-Confirmed Visual Content
Filters records where medical objects were detected in images.

![Confirmed Detections](./assets/api_confirmed_only.png)

---

### 3. Keyword-Based Medical Search
Supports case-insensitive and partial keyword search.

**Example:** Searching for `Marburg` returns all related outbreak updates.

![Search Results](./assets/api_search_results.png)

---

## 🛠️ Technical Highlights

### Data Cleaning

```python
def clean_text(text):
    """
    Removes URLs, emojis, advertisements, and non-medical noise.
    Normalizes Amharic and English text.
    """
    ...
````

---

### Database Security

All database access uses parameterized SQL queries to prevent SQL injection:

```python
query = text("""
    SELECT *
    FROM refined.medical_data
    WHERE cleaned_content ILIKE :key
""")

df = pd.read_sql(query, engine, params={"key": f"%{keyword}%"})
```

---

### Automated Documentation

API screenshots were generated automatically using Playwright to ensure documentation reflects real API responses.

---

## 📁 Project Structure

```text
.
├── api/
│   └── main.py
├── src/
├── medical_warehouse/
├── assets/
├── orchestrator.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

* Python 3.9+
* PostgreSQL
* Telegram API credentials

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/MAYSHLMAY/medical-telegram-warehouse.git
cd medical-telegram-warehouse
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
   Create a `.env` file:

```env
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
DB_HOST=localhost
DB_NAME=medical_warehouse
DB_USER=postgres
DB_PASSWORD=postgres
```

4. **Run the API**

```bash
uvicorn api.main:app --reload
```

5. **Open API documentation**

```
http://127.0.0.1:8000/docs
```

---

## ⏱️ Pipeline Orchestration

The entire pipeline is orchestrated using Dagster:

```bash
dagster dev -f orchestrator.py
```

Dagster provides:

* Visual data lineage
* Failure recovery and retries
* A single entry point for the full pipeline

---

## 📚 Learning Outcomes

* Modern ELT pipeline design
* Dimensional modeling (Star Schema)
* dbt testing and documentation
* Computer vision in data pipelines
* Secure API development
* Pipeline orchestration and observability

