# MoonWire Signal Engine v3 (Discovery Edition + Auto Loop)

---

## Overview

MoonWire is a real-time, autonomous crypto signal discovery engine.  
It scans the live crypto markets, detects price and volume anomalies (sleepers), and dispatches actionable signals automatically.

Built for real crypto-native traders who want speed, precision, and early mover advantage.

---

## Key Features

- **Fully live backend** — hosted cloud server (Render) scanning 24/7.
- **Real-time market discovery** — top 250 coins pulled live from CoinGecko.
- **Sleeper detection engine** — automatic identification of unexpected price/volume spikes.
- **Auto-run engine loop** — ingestion, analysis, and alerting every 10 minutes.
- **No manual inputs needed** — MoonWire runs autonomously once deployed.
- **Local cache memory (mock Redis)** — simplified and optimized for MVP.
- **Mobile-controllable** — test, trigger, and monitor via HTTPBot or Postman apps.

---

## Technology Stack 

- **FastAPI** — blazing-fast Python API server.
- **Uvicorn** — ASGI web server.
- **Requests** — for real-time API pulls from CoinGecko.
- **Python threading** — for background auto-run loops.
- **Render.com** — cloud deployment for API + automation.
- **GitHub** — version control and CI/CD for Render deployment.

---

## System Components

| Module | Purpose |
|:---|:---|
| `main.py` | FastAPI app entrypoint + background thread launcher |
| `src/ingest_discovery.py` | Pulls live top 250 crypto coins from CoinGecko |
| `src/signal_generator.py` | Analyzes assets for price/volume anomalies |
| `src/dispatcher.py` | Dispatches and logs sleeper signal alerts |
| `src/auto_loop.py` | Autonomous runner: ingestion → analysis → dispatch loop every 10 min |
| `src/cache.py` | Lightweight Python dictionary cache (no Redis server needed) |
| `src/logger.py` | Timestamped event logging for monitoring activity |

---

## How It Works

1. **Server Start:** FastAPI boots → Auto-loop thread launches.
2. **Every 10 minutes:**
   - Fetch live top 250 crypto coins.
   - Analyze each asset for sleepers.
   - Dispatch any matching sleeper signals to logs (future: to Email/SMS).
3. **Server Auto-Sleeps** (Render free plan) and Auto-Wakes as needed.

---

## Deployment Notes

- Hosted on **Render.com** (free/low-cost backend server).
- Redis is **mocked by local memory cache** for simplicity during MVP stage.
- Rate limiting protected by adjusting loop intervals (CoinGecko free API friendly).

---

## Next Upgrades

- Integrate **real Email/SMS alerting** (SendGrid, Twilio).
- Build **user-facing signal dashboard** (web frontend).
- Add **dynamic sentiment analysis** (Twitter/X or LunarCrush).
- Upgrade to managed Redis cloud when scaling past MVP.
- Offer **tiered access** (Free/Pro/Elite) with different signal privileges.

---

## Mission

> **Move faster than the crowd. Catch what others miss.  
> MoonWire.  
> Built for signal hunters.**

---

# End of Doc
