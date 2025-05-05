from datetime import datetime
from src.signal_filter import is_signal_valid
from src.cache_instance import cache
from src.sentiment_blended import blend_sentiment_scores

def generate_signals():
    print(f"[{datetime.utcnow()}] Running signal generation...")

    stablecoins = ["USDC", "USDT", "DAI", "TUSD", "BUSD"]
    assets = [k for k in cache.keys() if not k.endswith('_signals') and not k.endswith('_sentiment')]

    sentiment_scores = blend_sentiment_scores()
    valid_signals = []

    for asset in assets:
        if asset in stablecoins:
            continue

        data_list = cache.get_signal(asset)
        if not data_list:
            continue

        latest = data_list[-1]

        price_change = latest.get("price_change_24h")
        volume = latest.get("volume_now")

        if price_change is None or volume is None:
            continue

        sentiment = sentiment_scores.get(asset, 0.0)
        confidence = round(((price_change / 10) + sentiment) / 2, 2)

        signal = {
            "asset": asset,
            "movement": price_change,
            "volume": volume,
            "sentiment": sentiment,
            "confidence": confidence,
            "time": datetime.utcnow()
        }

        if is_signal_valid(signal):
            valid_signals.append(signal)

    return valid_signals