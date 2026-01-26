from fastapi import FastAPI
from routers.items import item_router
from uvicorn import run
from models.items import ItemModel
from contextlib import asynccontextmanager
from database import engine, Model

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    print("Database is ready")
    yield
    print("Shutting down server")

app = FastAPI(
    lifespan=lifespan,
    title="MyAPI",
    description="Learning to write backend",
    version="0.0.1"
)

app.include_router(item_router)

if __name__ == "__main__":
    run(app="main:app", host="127.0.0.1", port=8000, reload=True)