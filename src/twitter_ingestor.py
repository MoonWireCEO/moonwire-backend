# src/twitter_ingestor.py

import snscrape.modules.twitter as sntwitter
import os
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.cache_instance import cache
from fastapi import APIRouter, Query
import ssl
import tweepy

ssl._create_default_https_context = ssl._create_unverified_context

router = APIRouter()

def fetch_from_snscrape(query: str, limit: int = 5):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets.append(tweet.content)
    return tweets

def fetch_from_twitter_api(query: str, limit: int = 5):
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    client = tweepy.Client(bearer_token=bearer)
    resp = client.search_recent_tweets(query=query, tweet_fields=["created_at", "lang"], max_results=limit)
    return [t.text for t in resp.data or []]

def analyze_and_cache(asset: str, tweets: list[str]):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(t)["compound"] for t in tweets]
    avg = round(sum(scores) / len(scores), 4)

    cache.set_signal(f"{asset}_twitter_sentiment", {
        "sentiment": avg,
        "source": "Twitter",
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"asset": asset, "average_sentiment": avg, "tweets": tweets}

def fetch_tweets_and_analyze(asset: str, method="snscrape", limit=5):
    yesterday = (datetime.utcnow() - timedelta(days=1)).date()
    query = f"{asset} since:{yesterday}" if method == "snscrape" else asset

    if method == "snscrape":
        tweets = fetch_from_snscrape(query, limit)
    elif method == "api":
        tweets = fetch_from_twitter_api(query, limit)
    else:
        return {"error": f"Unknown method '{method}'"}

    if not tweets:
        return {"message": "No tweets found."}

    return analyze_and_cache(asset, tweets)

@router.get("/test-twitter")
def test_twitter(
    asset: str = Query("BTC"),
    method: str = Query("snscrape", enum=["snscrape", "api"]),
    limit: int = Query(5)
):
    return fetch_tweets_and_analyze(asset, method=method, limit=limit)