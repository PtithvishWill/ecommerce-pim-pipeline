import json
import sqlite3
import pandas as pd

DB_FILE = "pim_catalog.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            brand TEXT,
            completeness_score REAL,
            status TEXT,
            raw_attributes TEXT,
            variants_count INTEGER
        )
    """)
    conn.commit()
    conn.close()

def calculate_quality_score(product: dict) -> float:
    """Enforces Data Quality & Completeness Rules (PIM Governance)."""
    score = 0
    if product.get("name") and len(product["name"].strip()) > 3:
        score += 25
    if product.get("brand") and len(product["brand"].strip()) > 1:
        score += 25
    if product.get("attributes") and len(product["attributes"]) >= 2:
        score += 25
    if product.get("variants") and len(product["variants"]) > 0:
        score += 25
    return float(score)

def run_etl(feed_file="sample_supplier_feed.json"):
    """Ingest, cleanse, transform, and store supplier product feeds."""
    init_db()
    with open(feed_file, "r") as f:
        raw_feed = json.load(f)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    stats = {"ingested": 0, "published": 0, "quarantined": 0}

    for item in raw_feed:
        sku = item.get("supplier_sku")
        name = item.get("name", "").strip()
        category = item.get("category", "Uncategorized").strip()
        brand = item.get("brand", "").strip()
        attributes = json.dumps(item.get("attributes", {}))
        variants = item.get("variants", [])
        
        # Calculate PIM Data Quality Score
        quality_score = calculate_quality_score(item)
        status = "PUBLISHED" if quality_score >= 75.0 else "QUARANTINED"

        cursor.execute("""
            INSERT OR REPLACE INTO products 
            (product_id, name, category, brand, completeness_score, status, raw_attributes, variants_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (sku, name, category, brand, quality_score, status, attributes, len(variants)))

        stats["ingested"] += 1
        if status == "PUBLISHED":
            stats["published"] += 1
        else:
            stats["quarantined"] += 1

    conn.commit()
    conn.close()
    return stats

if __name__ == "__main__":
    results = run_etl()
    print("ETL Ingestion Complete:", results)
