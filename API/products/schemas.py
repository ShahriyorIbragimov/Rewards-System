from pydantic import BaseModel
from mixins import CreatedBy
from uuid import UUID

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    stock_quantity: int
    image_url: str
    category: str
    is_active: bool
    is_featured: bool
    sort_order: int
    created_by: CreatedBy

class ProductOut(ProductCreate):
    id: UUID

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    id: UUID
    name: str
    description: str
    price: int
    stock_quantity: int
    image_url: str
    category: str
    is_active: bool
    is_featured: bool
    sort_order: int
