from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="My API",
    description="I'm just fooling around with fastapi",
    version="1.0.0"
)

@app.get("/")
async def main():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)