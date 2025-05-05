import logging
from src.cache import SignalCache
from src.emailer import send_email_alert

logger = logging.getLogger(__name__)

def dispatch_alerts(asset: str, signal: dict, cache: SignalCache):
    logger.info(f"[Dispatch] Alert triggered for {asset}: {signal}")

    # Save signal to current slot
    cache.set_signal(f"{asset}_signals", signal)

    # Also append to historical log
    cache.add_to_history(asset, signal)

    # Prepare email
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