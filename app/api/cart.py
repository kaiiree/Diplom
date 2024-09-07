from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database_files import get_db
from app.database_files.models import Cart, Product
cart_router = APIRouter()


@cart_router.post("/cart/add/{product_id}")
async def add_to_cart(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.add(cart_item)

        db.commit()
        return {"message": "Product added to cart"}
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@cart_router.delete("/cart/remove/{product_id}")
async def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Product removed from cart"}


@cart_router.get("/{user_id}")
async def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return cart_items
