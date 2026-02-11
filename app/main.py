from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import Base, engine
from app.routers import items, purchase, slots


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Vending Machine API", lifespan=lifespan)

app.include_router(slots.router)
app.include_router(items.router)
app.include_router(purchase.router)


@app.get("/health")
def health():
    return {"status": "ok"}
