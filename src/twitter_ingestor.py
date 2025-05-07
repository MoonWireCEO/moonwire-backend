# src/twitter_ingestor.py

import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.cache_instance import cache
from fastapi import APIRouter

def fetch_tweets_and_analyze(asset: str, limit: int = 5):
    analyzer = SentimentIntensityAnalyzer()
    yesterday = (datetime.utcnow() - timedelta(days=1)).date()
    query = f"{asset} since:{yesterday}"

    try:
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            tweets.append(tweet.content)

        if not tweets:
            return {"message": "No tweets found."}

        scores = [analyzer.polarity_scores(text)["compound"] for text in tweets]
        average_score = round(sum(scores) / len(scores), 4)

        cache.set_signal(f"{asset}_twitter_sentiment", {
            "sentiment": average_score,
            "source": "Twitter",
            "timestamp": datetime.utcnow().isoformat()
        })

        return {"asset": asset, "average_sentiment": average_score, "tweets": tweets}

    except Exception as e:
        return {"error": str(e)}
        
router = APIRouter()

@router.get("/test-twitter")
def test_twitter():
    # You can change this asset string to test others
    return fetch_tweets_and_analyze("BTC")
