from datetime import datetime
from src.logger import log
from src.signal_filter import is_signal_valid
from src.cache_instance import cache  # Shared cache instance

def generate_signals():
    print(f"[{datetime.utcnow()}] Starting sleeper signal scan...")

    stablecoins = ["USDC", "USDT", "DAI", "TUSD", "BUSD"]

    assets = list(cache.cache.keys())
    assets = [a for a in assets if not a.endswith('_signals')]

    for asset in assets:
        print(f"[{datetime.utcnow()}] Scanning asset: {asset}")
        if asset in stablecoins:
            print(f"Skipping stablecoin: {asset}")
            continue

        data = cache.get_signal(asset)
        if not data:
            print(f"No data for asset: {asset}")
            continue

        price_change = data.get('price_change_24h')
        volume = data.get('volume_now')

        if price_change is None or volume is None:
            print(f"Incomplete data for {asset} — price or volume missing")
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
        else:
            print(f"Filtered out: {asset} | {price_change:.2f}% | ${volume:,.0f}")
