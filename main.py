# src/main.py

from fastapi import FastAPI
from src.twitter_router import router as twitter_router
from src.healthcheck import router as healthcheck_router
import uvicorn

app = FastAPI()

# Include routers
app.include_router(healthcheck_router)
app.include_router(twitter_router)

# Optional root route
@app.get("/")
def read_root():
    return {"status": "ok", "message": "MoonWire Signal Engine API is live."}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)