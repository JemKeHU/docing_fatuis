from fastapi import FastAPI
from router import item_router
from uvicorn import run

app = FastAPI(
    title="MyAPI",
    description="Learning to write backend",
    version="0.0.1"
)

app.include_router(item_router)

if __name__ == "__main__":
    run(app="main:app", host="127.0.0.1", port=8000, reload=True)