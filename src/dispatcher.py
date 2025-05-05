import logging
from src.cache import SignalCache
from src.emailer import send_email_alert

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def dispatch_alerts(asset: str, signal: dict, cache: SignalCache):
    """
    Dispatches alerts when a valid signal is detected.

    Args:
        asset (str): The asset symbol (e.g. BTC, ETH).
        signal (dict): The signal data triggering the alert.
        cache (SignalCache): Cache instance for storing state.
    """
    logger.info(f"[Dispatch] Alert triggered for {asset}: {signal}")

    # Save latest signal (overwrite)
    cache.set_signal(f"{asset}_signals", [signal])

    # Append to history (last 10)
    history_key = f"{asset}_history"
    history = cache.get_signal(history_key)
    history.append(signal)
    cache.set_signal(history_key, history[-10:])

    # Prepare email
    label = signal.get('confidence_label', 'Unknown Confidence')
    subject = f"MoonWire Alert: {asset} ({label})"
    body = (
        f"TEST ALERT:\n\n"
        f"Price moved {signal['price_change']}%\n"
        f"Volume: ${signal['volume']:,}\n"
        f"Sentiment Score: {signal['sentiment']:+.2f}\n"
        f"Confidence Score: {signal['confidence_score']:.2f} ({label})\n"
        f"Time: {signal['timestamp']} UTC\n"
    )

    # Send the alert
    send_email_alert(subject, body)

    # Log confirmation
    logger.info(f"[Signal Logged] {asset}: {signal}")