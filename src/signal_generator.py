from datetime import datetime
from src.signal_filter import is_signal_valid
from src.cache_instance import cache
from src.sentiment_blended import blend_sentiment_scores
from src.dispatcher import dispatch_alerts

def generate_signals():
    print(f"[{datetime.utcnow()}] Running signal generation...")

    stablecoins = ["USDC", "USDT", "DAI", "TUSD", "BUSD"]
    assets = [k for k in cache.keys() if not k.endswith('_signals') and not k.endswith('_sentiment')]

    sentiment_scores = blend_sentiment_scores()
    valid_signals = []

    for asset in assets:
        if asset in stablecoins:
            continue

        # Pull the latest signal — either a dict or last item from a list
        raw_data = cache.get_signal(asset)
        if not raw_data:
            continue

        data = raw_data[-1] if isinstance(raw_data, list) else raw_data
        if not isinstance(data, dict):
            continue

        price_change = data.get("price_change_24h")
        volume = data.get("volume_now")

        if price_change is None or volume is None:
            continue

        sentiment = sentiment_scores.get(asset, 0.0)
        confidence_score = round(((price_change / 10) + sentiment) / 2, 2)
        confidence_label = (
            "High Confidence" if confidence_score >= 0.6 else
            "Medium Confidence" if confidence_score >= 0.3 else
            "Low Confidence"
        )

        signal = {
            "asset": asset,
            "price_change": price_change,
            "volume": volume,
            "sentiment": sentiment,
            "confidence_score": confidence_score,
            "confidence_label": confidence_label,
            "timestamp": datetime.utcnow()
        }

        if is_signal_valid(signal):
            valid_signals.append(signal)

    for signal in valid_signals:
        dispatch_alerts(signal["asset"], signal, cache)