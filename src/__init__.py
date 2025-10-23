from fastapi import FastAPI
from .db.main import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
