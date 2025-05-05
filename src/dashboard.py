# src/dashboard.py

from fastapi import APIRouter
from src.cache_instance import cache
from src.sentiment_blended import blend_sentiment_scores
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/dashboard")
def dashboard():
    sentiment_scores = blend_sentiment_scores()
    output = {}

    logger.info(f"[Dashboard] Cache keys: {list(cache._store.keys())}")

    for key in cache._store:
        if key.endswith("_signals") or key.endswith("_sentiment"):
            continue

        asset = key
        history_key = f"{asset}_history"

        output[asset] = {
            "sentiment": sentiment_scores.get(asset, 0),
            "signals": cache.get_signal(asset),
            "history": cache.get_signal(history_key) or []
        }

        logger.info(f"[Dashboard] Asset: {asset}, History Key: {history_key}, Value: {output[asset]['history']}")

    return output