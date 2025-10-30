from typing import Optional
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
        ),
    )
    username: str = Field(index=True, unique=True, nullable=False)
    fullname: Optional[str] = None
    is_verified: bool = Field(default=False)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )
