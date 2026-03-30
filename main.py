from fastapi import FastAPI, Query, Path, HTTPException
import models as m
import db
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

tags_metadata = [
    {
        "name": "Categories",
        "description": "Operations with categories.",
    },
    {
        "name": "Products",
        "description": "Operations with products.",
    },
]


app = FastAPI()


@app.post("/create-category/", response_model=m.Category, tags=["Categories"])
def create_category(category: m.Category, session: db.SessionDep) -> m.Category:
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@app.get("/read-categories/", tags=["Categories"])
def read_categories(
    session: db.SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[m.Category]:
    categories = session.exec(select(m.Category).offset(offset).limit(limit)).all()
    return categories


@app.get("/read-category/{category_id}", tags=["Categories"])
def read_category(category_id: int, session: db.SessionDep) -> m.Category:
    category = session.get(m.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/update-category/{category_id}", tags=["Categories"])
def update_category(
    category_id: int, session: db.SessionDep, category_update: m.CategoryUpdate
):
    selected_category = session.get(m.Category, category_id)
    if not selected_category:
        raise HTTPException(status_code=404, detail="Category not found")
    selected_category.c_name = category_update.c_name
    session.commit()
    session.refresh(selected_category)
    return {category_id: f"has been updated to '{selected_category.c_name}'"}


@app.delete("/delete-category/{category_id}", tags=["Categories"])
def delete_category(category_id: int, session: db.SessionDep):
    category = session.get(m.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {category_id: "has been deleted"}


@app.post("/create-product/", response_model=m.Product, tags=["Products"])
def create_product(product: m.Product, session: db.SessionDep) -> m.Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@app.get("/read-products/", tags=["Products"])
def read_products(
    session: db.SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[m.Product]:
    products = session.exec(select(m.Product).offset(offset).limit(limit)).all()
    return products


@app.get("/read-product/{product_id}", tags=["Products"])
def read_product(product_id: int, session: db.SessionDep) -> m.Product:
    product = session.get(m.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/update-product/{product_id}", tags=["Products"])
def update_product(
    product_id: int, session: db.SessionDep, product_update: m.ProductUpdate
):
    selected_product = session.get(m.Product, product_id)
    if not selected_product:
        raise HTTPException(status_code=404, detail="Product not found")
    selected_product.p_name = product_update.p_name
    selected_product.price = product_update.price
    selected_product.category_id = product_update.category_id
    selected_product.description = product_update.description
    selected_product.create_date = product_update.create_date
    session.commit()
    session.refresh(selected_product)
    return {product_id: "has been updated"}


@app.delete("/delete-product/{product_id}", tags=["Products"])
def delete_product(product_id: int, session: db.SessionDep):
    product = session.get(m.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {product_id: "has been deleted"}
