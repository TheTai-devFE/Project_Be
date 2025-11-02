from fastapi import FastAPI
from .db.main import init_db, create_default_admin
from contextlib import asynccontextmanager
from src.Products.routes_catagory import cata_router
from src.Products.routes_product import product_router
from src.Auth.routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    await init_db()
    await create_default_admin()
    yield
    print("Shutting down...")


version = "v1"

app = FastAPI(lifespan=lifespan)


app.include_router(cata_router, prefix=f"/api/{version}/catagory", tags=["Categories"])
app.include_router(product_router, prefix=f"/api/{version}/product", tags=["Product"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
