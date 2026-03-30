from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from pydantic import BaseModel
import db


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    c_name: str = Field(index=True)
    products: list["Product"] = Relationship(back_populates="category")


class CategoryUpdate(BaseModel):
    c_name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    p_name: str = Field(index=True)
    price: float
    category_id: int = Field(foreign_key="category.id", index=True)
    category: Category = Relationship(back_populates="products")
    description: Optional[str] = Field(default=None)
    create_date: Optional[str] = Field(default=None)


class ProductUpdate(BaseModel):
    p_name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    create_date: Optional[str] = None
