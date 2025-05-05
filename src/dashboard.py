from fastapi import APIRouter
from src.cache_instance import cache

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    response = {}

    for key in cache.keys():
        if key.endswith("_signals") or key.endswith("_sentiment") or key.endswith("_history"):
            base_asset = key.split("_")[0]

            if base_asset not in response:
                response[base_asset] = {
                    "sentiment": [],
                    "signals": [],
                    "history": []
                }

            if key.endswith("_sentiment"):
                response[base_asset]["sentiment"].append(cache.get_signal(key))
            elif key.endswith("_signals"):
                response[base_asset]["signals"].append(cache.get_signal(key))
            elif key.endswith("_history"):
                response[base_asset]["history"] = cache.get_signal(key)

    return response