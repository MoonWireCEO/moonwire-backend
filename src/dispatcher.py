import logging
from src.cache import SignalCache
from src.emailer import send_email_alert

logger = logging.getLogger(__name__)

def dispatch_alerts(asset: str, signal: dict, cache: SignalCache):
    """
    Dispatches alerts when a valid signal is detected.
    Also logs the signal to the asset's history.
    """
    logger.info(f"[Dispatch] Alert triggered for {asset}: {signal}")

    # Save signal to cache
    cache.set_signal(asset, signal)

    # Append signal to history log
    history_key = f"{asset}_history"
    current_history = cache.get(history_key) or []
    current_history.append(signal)
    cache.set(history_key, current_history)

    # Format and send email alert
    label = signal.get("confidence_label", "Unknown Confidence")
    subject = f"MoonWire Alert: {asset} ({label})"
    body = (
        f"TEST ALERT:\n\n"
        f"Price moved {signal['price_change']}%\n"
        f"Volume: {signal['volume']}\n"
        f"Sentiment Score: {signal['sentiment']:.2f}\n"
        f"Confidence Score: {signal['confidence_score']:.2f} ({signal['confidence_label']})\n"
        f"Time: {signal['timestamp']} UTC\n"
    )
    send_email_alert(subject, body)

    logger.info(f"[Dispatch] Signal Logged: {signal}")