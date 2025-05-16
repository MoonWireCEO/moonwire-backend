from fastapi import APIRouter
from src.sentiment_news import fetch_news_sentiment_scores

router = APIRouter()

@router.get("/sentiment/news")
def get_news_sentiment_scores():
    return {"sentiment_scores": fetch_news_sentiment_scores()}