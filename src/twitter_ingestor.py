import os
import logging
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.cache_instance import cache
from fastapi import APIRouter, Query

router = APIRouter()
logging.basicConfig(level=logging.INFO)

# Always fallback to mock tweets
MOCK_TWEETS = [
    "Bitcoin is doing great today!",
    "People are hyped about BTC again.",
    "Market momentum looks strong for crypto.",
    "Feeling neutral on Bitcoin right now.",
    "Could go either way, but BTC sentiment seems positive."
]

def score_tweets(tweets: list[str]):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(t)["compound"] for t in tweets]
    return round(sum(scores) / len(scores), 4) if scores else 0.0

def fetch_tweets_and_analyze(asset: str, method="mock", limit=10):
    tweets = MOCK_TWEETS
    avg_sentiment = score_tweets(tweets)
    timestamp = datetime.utcnow().isoformat()

    cache.set_signal(f"{asset}_twitter_sentiment", {
        "sentiment": avg_sentiment,
        "source": "Twitter",
        "timestamp": timestamp
    })

    return {
        "asset": asset,
        "average_sentiment": avg_sentiment,
        "timestamp": timestamp,
        "source": "twitter",
        "sample_tweets": tweets
    }

@router.get("/sentiment/twitter")
def get_twitter_sentiment(
    asset: str = Query("BTC"),
    method: str = Query("mock", enum=["mock"]),
    limit: int = Query(10, ge=10, le=100)
):
    return fetch_tweets_and_analyze(asset, method=method, limit=limit)
