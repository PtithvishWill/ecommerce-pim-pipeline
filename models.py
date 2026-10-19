from pydantic import BaseModel, Field
from typing import Dict, List, Optional

# Variant Model (Child SKU)
class ProductVariant(BaseModel):
    sku: str
    price: float
    stock: int
    attributes: Dict[str, str] = Field(default_factory=dict)

# Master Product Model (Parent Entity)
class ProductMaster(BaseModel):
    product_id: str
    name: str
    category_hierarchy: str
    brand: str
    attributes: Dict[str, str]
    variants: List[ProductVariant]
    completeness_score: float = 0.0
    status: str = "DRAFT"  # DRAFT, PUBLISHED, QUARANTINED
