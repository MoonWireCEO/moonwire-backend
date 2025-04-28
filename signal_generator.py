from datetime import datetime
from src.logger import log

def generate_signals(cache):
    '''
    Generates sleeper trading signals across all cached assets.
    '''
    print(f"[{datetime.utcnow()}] Starting sleeper signal scan...")

    assets = cache.client.keys('*')  # All cached keys
    assets = [a.decode('utf-8') for a in assets if not a.endswith(b'_signals')]

    for asset in assets:
        data = cache.get_signal(asset)
        if not data:
            continue
        
        signals = []

        # Price movement detection
        if abs(data.get('price_change_24h', 0)) >= 5.0:
            signals.append(f"{asset}: Price moved {data['price_change_24h']:.2f}% in last 24h")

        # Volume surge detection
        if data.get('volume_now', 0) > 1000000:  # Minimum volume filter
            if data['volume_now'] > 2_000_000:  # 2x arbitrary "normal" baseline
                signals.append(f"{asset}: Volume surge to {data['volume_now']:.0f}")

        if signals:
            cache.set_signal(f"{asset}_signals", signals)
            log(f"[Signal Detected] {asset}: {signals}")