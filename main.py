from fastapi import FastAPI, HTTPException
import sqlite3
import json

app = FastAPI(
    title="Product Information Management (PIM) API",
    description="REST API for Product Taxonomy, Variant Syndication, and Data Quality Auditing",
    version="1.0.0"
)

DB_FILE = "pim_catalog.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"message": "PIM Service is operational", "docs": "/docs"}

@app.get("/catalog")
def get_published_catalog():
    """Retrieve all high-quality published products ready for digital channels."""
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products WHERE status = 'PUBLISHED'").fetchall()
    conn.close()
    return [dict(p) for p in products]

@app.get("/products/{product_id}")
def get_product_by_id(product_id: str):
    """Retrieve a single master product record with attributes."""
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    data = dict(product)
    data["raw_attributes"] = json.loads(data["raw_attributes"])
    return data

@app.get("/governance/quarantine")
def get_quarantined_products():
    """Audit items flagged by Data Stewardship due to poor completeness score."""
    conn = get_db_connection()
    quarantined = conn.execute("SELECT * FROM products WHERE status = 'QUARANTINED'").fetchall()
    conn.close()
    return [dict(q) for q in quarantined]
