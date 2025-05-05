from fastapi import APIRouter
from src.cache_instance import cache
from src.sentiment_blended import blend_sentiment_scores

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    sentiment_scores = blend_sentiment_scores()
    output = {}

    for key in cache._store:
        if key.endswith("_signals") or key.endswith("_sentiment"):
            continue

        asset = key
        output[asset] = {
            "sentiment": sentiment_scores.get(asset, 0),
            "signals": cache.get_signal(asset),
            "history": cache.get_signal(f"{asset}_history") or []
        }

    return output