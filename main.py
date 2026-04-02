from fastapi import FastAPI, Query, Path, HTTPException
import models as m
import db
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


@app.post("/categories/", response_model=m.CategoryCreate, tags=["Categories"])
def create_category(
    category: m.CategoryCreate, session: db.SessionDep
) -> m.CategoryCreate:
    cat = m.Category()
    cat.c_name = category.c_name
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@app.get("/categories/", response_model=list[m.Category], tags=["Categories"])
def read_categories(
    session: db.SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[m.Category]:
    categories = session.exec(select(m.Category).offset(offset).limit(limit)).all()
    return categories


@app.get("/categories/{category_id}", response_model=m.Category, tags=["Categories"])
def read_category(category_id: int, session: db.SessionDep) -> m.Category:
    category = session.get(m.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put(
    "/categories/{category_id}", response_model=m.CategoryUpdate, tags=["Categories"]
)
def update_category(
    category_id: int, session: db.SessionDep, category_update: m.CategoryUpdate
):
    selected_category = session.get(m.Category, category_id)
    if not selected_category:
        raise HTTPException(status_code=404, detail="Category not found")
    selected_category.c_name = category_update.c_name
    session.commit()
    session.refresh(selected_category)
    return selected_category


@app.delete("/categories/{category_id}", response_model=m.Category, tags=["Categories"])
def delete_category(category_id: int, session: db.SessionDep):
    category = session.get(m.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return category


@app.post(
    "/products/",
    response_model=m.ProductCreate,
    tags=["Products"],
)
def create_product(product: m.ProductCreate, session: db.SessionDep) -> m.ProductCreate:
    prod = m.Product()
    prod.p_name = product.p_name
    prod.price = product.price
    prod.category_id = product.category_id
    prod.description = product.description
    prod.create_date = product.create_date
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod


@app.get("/products/", response_model=list[m.Product], tags=["Products"])
def read_products(
    session: db.SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[m.Product]:
    products = session.exec(select(m.Product).offset(offset).limit(limit)).all()
    return products


@app.get("/products/{product_id}", response_model=m.Product, tags=["Products"])
def read_product(product_id: int, session: db.SessionDep) -> m.Product:
    product = session.get(m.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=m.ProductUpdate, tags=["Products"])
def update_product(
    product_id: int, session: db.SessionDep, product_update: m.ProductUpdate
):
    selected_product = session.get(m.Product, product_id)
    if not selected_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_update.p_name is not None:
        selected_product.p_name = product_update.p_name
    if product_update.price is not None:
        selected_product.price = product_update.price
    if product_update.category_id is not None:
        selected_product.category_id = product_update.category_id
    if product_update.description is not None:
        selected_product.description = product_update.description
    if product_update.create_date is not None:
        selected_product.create_date = product_update.create_date
    session.commit()
    session.refresh(selected_product)
    return selected_product


@app.delete("/products/{product_id}", response_model=m.Product, tags=["Products"])
def delete_product(product_id: int, session: db.SessionDep):
    product = session.get(m.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return product
