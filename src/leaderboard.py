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
    
def get_movement_label(change: float) -> str:
    if change >= 10:
        return "Exploding"
    elif change >= 5:
        return "Surging"
    elif change >= 2:
        return "Moving"
    elif change > -2:
        return "Stable"
    elif change >= -5:
        return "Falling"
    else:
        return "Crashing"

@router.get("/leaderboard")
def leaderboard():
    output = []
    for key in cache.keys():
        if not key.endswith("_history"):
            history = cache.get_signal(f"{key}_history") or []
            if history:
                latest = history[-1]
                output.append({
                    "asset": key,
                    "price_change": latest.get("price_change", 0),
                    "sentiment": latest.get("sentiment", 0),
                    "confidence_score": latest.get("confidence_score", 0),
                    "timestamp": latest.get("timestamp", ""),
                    "movement_label": get_movement_label(latest.get("price_change", 0))
                })
            else:
                output.append({
                    "asset": key,
                    "price_change": 0,
                    "sentiment": 0,
                    "confidence_score": 0,
                    "timestamp": "",
                    "movement_label": "No Data"
                })
    return sorted(output, key=lambda x: x["price_change"], reverse=True)