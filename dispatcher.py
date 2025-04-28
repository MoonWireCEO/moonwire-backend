from src.logger import log

def dispatch_alerts(cache):
    assets = ['BTC', 'ETH', 'SOL']
    for asset in assets:
        signals = cache.get_signal(f"{asset}_signals")
        if signals:
            for signal in signals:
                log(f"[ALERT] {signal}")
            # Optionally clear signals after dispatch to prevent re-sending
            cache.delete_signal(f"{asset}_signals")