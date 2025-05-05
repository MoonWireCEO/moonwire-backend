# src/dashboard.py

from fastapi import APIRouter
from src.cache_instance import cache

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    assets = ["BTC", "ETH", "SOL", "ADA", "DOGE", "TEST"]  # Adjust as needed

    response = {}

    for asset in assets:
        sentiment_key = f"{asset}_sentiment"
        signals_key = f"{asset}_signals"

        sentiment = cache.get_signal(sentiment_key)
        signals = cache.get_signal(signals_key)

        response[asset] = {
            "sentiment": sentiment,
            "signals": [],
            "history": []
        }

        if signals:
            response[asset]["signals"] = signals

        if isinstance(signals, list):
            history = []
            for signal in signals:
                history.append({
                    "timestamp": signal.get("timestamp"),
                    "price_change": signal.get("price_change"),
                    "volume": signal.get("volume"),
                    "sentiment": signal.get("sentiment"),
                    "confidence_score": signal.get("confidence_score"),
                    "confidence_label": signal.get("confidence_label")
                })
            response[asset]["history"] = history

    return response