from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.twitter_router import router as twitter_router
from src.healthcheck import router as healthcheck_router
from src.news_router import router as news_router  # Added import
import uvicorn

app = FastAPI()

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://moonwire-frontend-clean.vercel.app",
        "https://moonwire-frontend-clean-5lf0ebne1-andrews-projects-3d597529.vercel.app",
        "*",  # Consider tightening this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(healthcheck_router)
app.include_router(twitter_router)
app.include_router(news_router)  # Added router registration

# Optional root route
@app.get("/")
def read_root():
    return {"status": "ok", "message": "MoonWire Signal Engine API is live."}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)