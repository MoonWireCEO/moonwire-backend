# dispatcher.py

from fastapi import APIRouter
from datetime import datetime
from src.cache import SignalCache
from src.utils.logging import log_signal

router = APIRouter()
cache = SignalCache()

@router.get("/dispatch")
async def dispatch_signals():
    assets = ["BTC", "ETH", "SOL", "ADA", "DOGE", "TEST"]
    dispatched = {}

    for symbol in assets:
        signals = cache.get_signals(symbol)
        if signals:
            dispatched[symbol] = signals
            for signal in signals:
                log_signal(signal)
            print(f"[Dispatch] Dispatched {len(signals)} signals for {symbol}")
        else:
            print(f"[Dispatch] No signals found for {symbol}")

    return {"dispatched": dispatched}


@router.post("/test-alert")
async def test_alert():
    signal = {
        "symbol": "TEST",
        "confidence": 0.62,
        "sentiment_score": 0.0,
        "price_change": 12.5,
        "volume": 50000000,
        "timestamp": datetime.utcnow().isoformat(),
        "notes": "Manual test alert"
    }

    log_signal(signal)
    cache.store_signal("TEST", signal)
    print("[Dispatcher] Test alert sent to dispatcher")
    return {"message": "Test alert dispatched"}

