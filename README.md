# MoonWire Signal Engine v2  
**Internal Documentation**

---

## Overview

MoonWire Signal Engine v2 is the **real-time backend system** that ingests crypto market data, generates actionable trading signals, and dispatches alerts automatically.

This system forms the **core technical brain** of MoonWire's MVP and early product launch.

---

## System Components

| Module | Purpose |
|:---|:---|
| `main.py` | FastAPI app to manage endpoints and lifecycle |
| `src/ingest.py` | Placeholder for future real data ingestion (Binance, CoinGecko) |
| `src/fake_ingest.py` | Simulates BTC, ETH, SOL market data every 60 seconds |
| `src/signal_generator.py` | Applies simple signal detection rules (price, volume, sentiment) |
| `src/dispatcher.py` | Dispatches generated alerts (console logs now, SMS/Email later) |
| `src/auto_trigger.py` | Automatically runs Ingest → Signal → Dispatch loop forever |
| `src/cache.py` | Redis-backed fast cache for market data and signals |
| `src/logger.py` | UTC timestamped event logging |

---

## How It Works

1. **Startup**  
   - FastAPI server boots up.
   - `auto_run()` starts in a background thread.

2. **Ingest Loop (every 60 sec)**  
   - Fake market data (price, volume, sentiment) for BTC, ETH, SOL is generated and saved into cache.

3. **Signal Generation**  
   - For each asset, engine checks if any triggers are met:
     - Price spike (+3% 1hr move)
     - Volume surge (+50% above average)
     - Sentiment spike (+20% 6hr move)
   - If so, it creates signal messages.

4. **Dispatch**  
   - Any signals found are logged as alerts.
   - (Later: Will integrate with SMS, Email, Discord, etc.)

---

## Deployment Notes

- **Redis** must be running (`localhost:6379` by default).
- **FastAPI server** must be launched (`uvicorn main:app --reload`).
- **Threaded auto-run** ensures ingestion and signal generation without manual triggers.

---

## Next Development Steps

- Replace `fake_ingest.py` with real API ingestion.
- Build real user notification systems (SMS, Email, Push).
- Add user-specific signal thresholds (Pro/Elite tier logic).
- Add error handling, retries, resilience features.

---

## Mission Critical

This engine ensures MoonWire's **real-time intelligence promise**:
> "Move faster than the crowd — on true market signals, not noise."

---

# End of Doc