def dispatch_alerts(asset: str, signal: dict, cache: SignalCache):
    logger.info(f"[Dispatch] Alert triggered for {asset}: {signal}")

    # Save to signal + history
    cache.set_signal(asset, signal)
    cache.set_history(asset, signal)

    # Email
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