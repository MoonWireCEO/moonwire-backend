# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.twitter_router import router as twitter_router
from src.healthcheck import router as healthcheck_router

app = FastAPI()

# Enable CORS for all origins (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(twitter_router, prefix="/sentiment")
app.include_router(healthcheck_router)

@app.get("/")
def read_root():
    return {"message": "MoonWire Signal Engine is live!"}