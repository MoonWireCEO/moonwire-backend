# src/signal_generator.py

from datetime import datetime
from src.logger import log
from src.signal_filter import is_signal_valid

def generate_signals(cache):
    print(f"[{datetime.utcnow()}] Starting sleeper signal scan...")

    stablecoins = ["USDC", "USDT", "DAI", "TUSD", "BUSD"]

    assets = list(cache.cache.keys())
    assets = [a for a in assets if not a.endswith('_signals')]

    for asset in assets:
        if asset in stablecoins:
            continue

        data = cache.get_signal(asset)
        if not data:
            continue

        price_change = data.get('price_change_24h')
        volume = data.get('volume_now')

        if price_change is None or volume is None:
            continue

        signal = {
            'asset': asset,
            'movement': price_change,
            'volume': volume,
            'time': datetime.utcnow()
        }

        if is_signal_valid(signal):
            cache.set_signal(f"{asset}_signals", [signal])
            log(f"[Signal Detected] {asset}: {signal}")
