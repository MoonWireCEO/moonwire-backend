from datetime import datetime
from src.logger import log

def generate_signals(cache):
    '''
    Generates sleeper trading signals across all cached assets.
    '''
    print(f"[{datetime.utcnow()}] Starting sleeper signal scan...")

    stablecoins = ["USDC", "USDT", "DAI", "TUSD", "BUSD"]

    assets = list(cache.cache.keys())
    assets = [a for a in assets if not a.endswith('_signals')]

    for asset in assets:
        if asset in stablecoins:
            continue  # Skip stablecoins

        data = cache.get_signal(asset)
        if not data:
            continue  # Skip if no data

        signals = []

        # Only scan coins with sufficient volume
        if data.get('volume_now') is not None and data['volume_now'] > 10_000_000:

            # Detect major price movement (now requiring 7% move)
            if data.get('price_change_24h') is not None:
                if abs(data['price_change_24h']) >= 7.0:
                    signals.append(f"{asset}: Price moved {data['price_change_24h']:.2f}% in last 24h")

            # Detect extreme volume surges separately
            if data['volume_now'] > 20_000_000:
                signals.append(f"{asset}: Volume surge to {data['volume_now']:.0f}")

        if signals:
            cache.set_signal(f"{asset}_signals", signals)
            log(f"[Signal Detected] {asset}: {signals}")

