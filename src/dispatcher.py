# src/dashboard.py

from fastapi import APIRouter
from src.cache_instance import cache

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    data = {}

    for key in cache.keys():
        # Expecting keys like "BTC_signals", "BTC_history", "BTC_sentiment"
        if "_" not in key:
            continue

        asset, data_type = key.split("_", 1)

        if asset not in data:
            data[asset] = {
                "sentiment": 0,
                "signals": [],
                "history": []
            }

        if data_type == "sentiment":
            data[asset]["sentiment"] = cache.get_signal(key)
        elif data_type == "signals":
            data[asset]["signals"] = cache.get_signal(key)
        elif data_type == "history":
            data[asset]["history"] = cache.get_signal(key)

    return data