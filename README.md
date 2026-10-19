# Enterprise E-Commerce PIM & Catalog ETL Pipeline

An end-to-end Product Information Management (PIM) solution built with **Python**, **FastAPI**, **SQL (SQLite)**, and **Pydantic**. Designed to ingest unstructured supplier feeds, enforce product data governance and attribute completeness scores, and syndicate high-quality catalog data to digital eCommerce channels via RESTful APIs.

## Architecture & Data Flow
1. **Data Ingestion (ETL):** Ingests raw JSON supplier feeds containing products, categories, dynamic attributes, and child SKU variants.
2. **Data Governance & Quality Scoring:** Evaluates mandatory fields (brand, SKU, attributes, variants) and calculates a **Completeness Score (0–100%)**.
3. **Data Stewardship Quarantine:** Products scoring `< 75%` completeness are automatically flagged and routed to a **Quarantine** queue for data steward review.
4. **Catalog Syndication (REST API):** High-quality, published product models and variants are stored in an analytical SQL database and exposed via FastAPI endpoints for eCommerce digital channels.

## Tech Stack
* **Language & Backend:** Python 3, FastAPI, Uvicorn
* **Data Validation:** Pydantic
* **Database & Querying:** SQL (SQLite / MySQL schema design), Pandas
* **API Documentation:** OpenAPI 3.0 / Swagger UI

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the ETL & Data Quality Pipeline
```bash
python etl.py
```
*Expected Output:*
```text
ETL Ingestion Complete: {'ingested': 3, 'published': 2, 'quarantined': 1}
```

### 3. Start the PIM REST API Server
```bash
uvicorn main:app --reload
```

### 4. Interactive Swagger API Docs
Open your browser and navigate to:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **`GET /catalog`**: Export all verified, published catalog products.
* **`GET /products/{id}`**: Inspect product attributes and variants.
* **`GET /governance/quarantine`**: Review products needing data stewardship intervention.
