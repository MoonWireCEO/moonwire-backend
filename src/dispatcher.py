import logging
from src.cache import SignalCache
from src.emailer import send_email_alert

logger = logging.getLogger(__name__)

def dispatch_alerts(asset: str, signal: dict, cache: SignalCache):
    """
    Dispatches alerts when a valid signal is detected.

    Args:
        asset (str): The asset symbol (e.g. BTC, ETH).
        signal (dict): The signal data triggering the alert.
        cache (SignalCache): Cache instance for storing state.
    """
    logger.info(f"[Dispatch] Alert triggered for {asset}: {signal}")

    # Save signal to cache
    cache.set_signal(asset, signal)

    # Save to history
    history_key = f"{asset}_history"
    history = cache.get_signal(history_key) or []
    history.append(signal)
    cache.set_signal(history_key, history)

    # Format and send email alert
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

    logger.info(f"[Signal Logged] {signal}")