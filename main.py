from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="I'm just fooling around with fastapi",
    version="1.0.0"
)

@app.get("/")
async def main():
    return {"message": "Hello World!"}