# src/leaderboard.py

from fastapi import APIRouter
from src.cache_instance import cache

router = APIRouter()

@router.get("/leaderboard")
def leaderboard():
    leaderboard_data = []

    for key in cache._store.keys():
        if key.endswith("_signals") or key.endswith("_sentiment") or key.endswith("_history"):
            continue

        signals = cache.get_signal(key)
        if not signals:
            continue

        latest = signals[-1] if isinstance(signals, list) else signals

        leaderboard_data.append({
            "asset": key,
            "price_change": latest.get("price_change", 0),
            "sentiment": latest.get("sentiment", 0),
            "confidence_score": latest.get("confidence_score", 0),
            "timestamp": latest.get("timestamp", "")
        })

    # Sort by absolute price change (biggest movers first)
    leaderboard_data.sort(key=lambda x: abs(x["price_change"]), reverse=True)

    return leaderboard_data[:5]  # Top 5