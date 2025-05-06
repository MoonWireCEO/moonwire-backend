# src/leaderboard.py

from fastapi import APIRouter, Query
from src.cache_instance import cache

router = APIRouter()

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
def leaderboard(
    sort_by: str = Query("price_change", enum=["price_change", "sentiment", "confidence_score", "timestamp"]),
    descending: bool = Query(True)
):
    output = []
    for key in cache.keys():
        if not key.endswith("_history"):
            history = cache.get_signal(f"{key}_history")
            if isinstance(history, list) and history:
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

    return sorted(output, key=lambda x: x.get(sort_by, 0) or 0, reverse=descending)