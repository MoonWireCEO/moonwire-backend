import logging
from datetime import datetime
from src.cache import SignalCache
from src.emailer import send_email_alert

logger = logging.getLogger(__name__)

def dispatch_alerts(asset: str, signal: dict, cache: SignalCache):
    """
    Dispatches alerts when a valid signal is detected.
    """
    logger.info(f"[Dispatch] Alert triggered for {asset}: {signal}")

    # Save signal to cache
    cache.set_signal(asset, signal)

    # Save to history
    history_key = f"{asset}_history"
    history = cache.get_signal(history_key)
    if not isinstance(history, list):
        history = []
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "signal": signal
    })
    cache.set_signal(history_key, history)

    # Email Alert
    label = signal.get("confidence_label", "Unknown Confidence")
    subject = f"MoonWire Alert: {asset} ({label})"
    body = (
        f"TEST ALERT:\n\n"
        f"Price moved {signal['price_change']}%\n"
        f"Volume: ${signal['volume']:,}\n"
        f"Sentiment Score: {signal['sentiment']:+.2f}\n"
        f"Confidence Score: {signal['confidence_score']:.2f} ({label})\n"
        f"Time: {signal['timestamp']} UTC\n"
    )
    send_email_alert(subject, body)

    logger.info(f"[Signal Logged] TEST: {signal}")