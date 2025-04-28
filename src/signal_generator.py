from datetime import datetime
from src.logger import log

def generate_signals(cache):
    '''
    Generates sleeper trading signals across all cached assets.
    '''
    print(f"[{datetime.utcnow()}] Starting sleeper signal scan...")

    assets = list(cache.cache.keys())
    assets = [a for a in assets if not a.endswith('_signals')]

    for asset in assets:
        data = cache.get_signal(asset)
        if not data:
            continue  # Skip if no data

        signals = []

        # Defensive check for price movement
        if data.get('price_change_24h') is not None:
            if abs(data['price_change_24h']) >= 5.0:
                signals.append(f"{asset}: Price moved {data['price_change_24h']:.2f}% in last 24h")

        # Defensive check for volume
        if data.get('volume_now') is not None:
            if data['volume_now'] > 1000000:
                if data['volume_now'] > 2_000_000:
                    signals.append(f"{asset}: Volume surge to {data['volume_now']:.0f}")

        if signals:
            cache.set_signal(f"{asset}_signals", signals)
            log(f"[Signal Detected] {asset}: {signals}")