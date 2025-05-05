from fastapi import APIRouter
from src.cache_instance import cache

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    assets = ["BTC", "ETH", "SOL", "ADA", "DOGE", "TEST"]
    response = {}

    for asset in assets:
        sentiment = cache.get_signal(f"{asset}_sentiment")
        signal = cache.get_signal(f"{asset}_signals")
        history = cache.get_signal(f"{asset}_history")

        response[asset] = {
            "sentiment": sentiment,
            "signals": signal,
            "history": history
        }

    return response