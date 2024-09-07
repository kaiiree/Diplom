from fastapi import FastAPI, Request
# from starlette.middleware.sessions import SessionMiddleware
from app.api import products, auth, cart
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database_files import Base, engine, get_db
from app.database_files.models import Product
from config import templates


app = FastAPI(docs_url="/admin")
Base.metadata.create_all(engine)
app.mount("/static/css", StaticFiles(directory="app/static/css"), name="static")

# app.add_middleware(SessionMiddleware, secret_key="684")

# Подключаем роутеры
app.include_router(auth.auth_router, prefix="/auth")
app.include_router(products.prod_router, prefix="/api")
app.include_router(cart.cart_router, prefix='/cart')


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db = next(get_db())
    all_products = db.query(Product).all()
    print()
    return templates.TemplateResponse(request, "index.html", context={"all_product": all_products})
