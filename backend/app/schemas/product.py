from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class InProduct(BaseModel):
    name: str
    slug: str
    description: str
    price_cents: int = Field(..., ge=0, description="Price in cents (e.g., $19.99 → 1999)")
    currency: str = "USD"
    inventory: int = 0
    is_active: bool = True
    data: Optional[Dict] = Field(default_factory=dict)

    class Config:
        extra = "forbid"  # avoid silent errors on unexpected fields


class OutProduct(InProduct):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
