from typing import Optional, List
from pydantic import BaseModel
import uuid
from datetime import datetime


class CategoryModel(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateCategoryModel(BaseModel):
    name: str


class ProductModel(BaseModel):
    uid: uuid.UUID
    name: str
    code: str
    description: str
    price: float
    min_price: float
    stock: int
    lowstock: int
    spess: Optional[dict] = None
    # category_uid: Optional[uuid.UUID] = None
    category: Optional[CategoryModel] = None
    image_urls: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductCreateModel(BaseModel):
    name: str
    code: str
    description: str
    price: float
    min_price: float
    stock: int
    lowstock: int
    spess: Optional[dict] = None
    category_uid: Optional[uuid.UUID] = None
    image_urls: Optional[List[str]] = None


class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    min_price: Optional[float] = None
    stock: Optional[int] = None
    lowstock: Optional[int] = None
    spess: Optional[dict] = None
    category_uid: Optional[uuid.UUID] = None
    image_urls: Optional[List[str]] = None
