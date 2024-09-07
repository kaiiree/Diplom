from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database_files import get_db
from app.database_files.models import Product
from config import templates

prod_router = APIRouter()


@prod_router.get("/products")
async def get_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@prod_router.post("/products")
async def create_product(name: str, description: str, price: int, db: Session = Depends(get_db)):
    product = Product(name=name, description=description, price=price)
    db.add(product)
    db.commit()
    return product


@prod_router.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@prod_router.put("/products/{product_id}")
async def update_product(product_id: int, name: str, description: str, price: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = name
    product.description = description
    product.price = price
    db.commit()
    return product


@prod_router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}

