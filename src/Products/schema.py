from typing import Optional, List
from pydantic import BaseModel
import uuid
from datetime import datetime


class CategoryModel(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime


class CreateCategoryModel(BaseModel):
    name: str


class ImageProductModel(BaseModel):
    uid: uuid.UUID
    product_uid: Optional[uuid.UUID]
    main_image: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProductImageCreate(BaseModel):
    main_image: Optional[str] = None
    image_url: Optional[str] = None


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
    category_uid: Optional[uuid.UUID] = None
    images: Optional[List[ProductImageCreate]] = None
    created_at: datetime
    updated_at: datetime


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
    images: Optional[List[ImageProductModel]] = None
