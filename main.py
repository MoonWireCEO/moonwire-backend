from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.twitter_router import router as twitter_router
from src.healthcheck import router as healthcheck_router
from src.sentiment_news_router import router as news_router
import uvicorn

app = FastAPI()

# CORS Middleware — Temporary Open Access for Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary: Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Register API routes
app.include_router(healthcheck_router)
app.include_router(twitter_router)
app.include_router(news_router)

# Root Route for Quick API Status Check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "MoonWire Signal Engine API is live."}

# Local Run Entry Point (Optional)
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)