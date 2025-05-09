from fastapi import APIRouter, Query
from src.twitter_ingestor import fetch_tweets_and_analyze

router = APIRouter()

@router.get("/sentiment/twitter")
def get_twitter_sentiment(
    asset: str = Query("BTC"),
    method: str = Query("snscrape", enum=["snscrape", "api"]),
    limit: int = Query(10, ge=10, le=100)
):
    return fetch_tweets_and_analyze(asset, method=method, limit=limit)