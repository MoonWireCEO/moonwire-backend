from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import twitter_router
from src import news_router  # Corrected import name

app = FastAPI()

# Allow any origin - temporary for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(twitter_router.router)
app.include_router(news_router.router)  # Corrected usage