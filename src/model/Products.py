from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class Product(SQLModel, table=True):

    __tablename__ = "products"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID, primary_key=True, unique=True, nullable=False),
    )
    name: str = Field(sa_column=Column(pg.VARCHAR(100), default="Name Products"))
    code: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    description: str
    price: float = Field(default=0)
    min_price: float = Field(default=0)
    stock: int = Field(default=0)
    lowstock: int = Field(default=5)

    spess: Optional[dict] = Field(sa_column=Column(pg.JSON, default=None))

    category_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="product_categories.uid"
    )
    image_urls: Optional[List[str]] = Field(
        default=None, sa_column=Column(pg.JSON, nullable=True)
    )

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )

    # Relationship
    category: Optional["ProductCategory"] = Relationship(
        back_populates="products", sa_relationship_kwargs={"lazy": "selectin"}
    )


class ProductCategory(SQLModel, table=True):
    __tablename__ = "product_categories"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID, primary_key=True, unique=True, nullable=False),
    )

    name: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )

    # Relationship
    products: List["Product"] = Relationship(back_populates="category")
