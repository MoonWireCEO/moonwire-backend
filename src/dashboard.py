from fastapi import APIRouter
from src.cache_instance import cache

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    tracked_assets = ['BTC', 'ETH', 'SOL', 'ADA', 'DOGE', 'TEST']
    dashboard = {}

    for asset in tracked_assets:
        sentiment = cache.get_signal(f"{asset}_sentiment") or 0.0
        signals = cache.get_signal(f"{asset}_signals") or []

        dashboard[asset] = {
            "sentiment": round(sentiment, 4),
            "signals": signals
        }

    return dashboard
