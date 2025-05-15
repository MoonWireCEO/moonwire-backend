import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def scrape_tweets_with_snscrape(asset: str) -> Optional[Dict]:
    # Simulated snscrape logic (replace with real scraping if applicable)
    raise Exception("SSL verification failed (simulated)")  # Simulate failure for demonstration
    # return {"asset": asset, "source": "snscrape", "sample_tweets": ["..."]}

def fetch_tweets_with_twitter_api(query: str) -> Optional[Dict]:
    # Simulated API fetch logic (replace with real API call if applicable)
    logger.info(f"Fetching tweets with Twitter API using query: {query}")
    # Simulate empty or rate-limited response for demonstration
    return {"asset": query.split()[0], "source": "twitter_api", "sample_tweets": ["Sample tweet 1", "Sample tweet 2"]}

def mock_tweet_response(asset: str) -> Dict:
    return {
        "asset": asset,
        "average_sentiment": 0.4014,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "mock",
        "sample_tweets": [
            "Bitcoin is doing great today!",
            "People are hyped about BTC again.",
            "Market momentum looks strong for crypto.",
            "Feeling neutral on Bitcoin right now.",
            "Could go either way, but BTC sentiment seems positive.",
        ]
    }

def fetch_tweets(asset: str, method: Optional[str] = None) -> Dict:
    if method == "mock":
        return mock_tweet_response(asset)

    # First attempt: snscrape
    try:
        tweets = scrape_tweets_with_snscrape(asset)
        if tweets:
            return tweets
    except Exception as e:
        logger.error(f"snscrape failed: {e}")

    # Second attempt: Twitter API (without cashtag operator)
    try:
        search_query = f"{asset} lang:en"  # Removed cashtag operator ($)
        tweets = fetch_tweets_with_twitter_api(search_query)
        if tweets:
            return tweets
    except Exception as e:
        logger.error(f"Twitter API fetch failed: {e}")

    # Final fallback: Mock data
    return mock_tweet_response(asset)