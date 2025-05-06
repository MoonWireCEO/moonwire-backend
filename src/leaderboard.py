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
def leaderboard(sort_by: str = Query("price_change")):
    output = []
    for key in cache._store:
        if not key.endswith("_history"):
            history = cache.get_signal(f"{key}_history")
            if history:
                latest = history[-1]
                output.append({
                    "asset": key,
                    "price_change": latest.get("price_change", 0),
                    "sentiment": latest.get("sentiment", 0),
                    "confidence_score": latest.get("confidence_score", 0),
                    "timestamp": latest.get("timestamp", ""),
                    "movement_label": get_movement_label(latest.get("price_change", 0)),
                })
            else:
                output.append({
                    "asset": key,
                    "price_change": 0,
                    "sentiment": 0,
                    "confidence_score": 0,
                    "timestamp": "",
                    "movement_label": "No Data",
                })

    valid_keys = {"price_change", "sentiment", "confidence_score", "timestamp"}
    sort_key = sort_by if sort_by in valid_keys else "price_change"

    return sorted(output, key=lambda x: x.get(sort_key, 0), reverse=True)