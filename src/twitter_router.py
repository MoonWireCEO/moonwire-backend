# src/routers/twitter_router.py

from fastapi import APIRouter, Query
from src.twitter_ingestor import fetch_tweets_and_analyze

router = APIRouter()

@router.get("/sentiment/twitter")
def get_twitter_sentiment(
    asset: str = Query(..., description="Asset symbol, e.g., BTC, ETH"),
    method: str = Query("snscrape", enum=["snscrape", "api"], description="Fetch method: snscrape or api"),
    limit: int = Query(10, ge=10, le=100, description="Number of tweets to analyze")
):
    """
    Get average sentiment for a specific asset from Twitter.
    """
    result = fetch_tweets_and_analyze(asset, method=method, limit=limit)

    return {
        "asset": result["asset"],
        "average_sentiment": result["average_sentiment"],
        "timestamp": None,
        "source": "twitter",
        "sample_tweets": result["tweets"]
    }