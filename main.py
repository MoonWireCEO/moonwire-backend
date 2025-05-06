from fastapi import FastAPI, BackgroundTasks
from threading import Thread
from datetime import datetime
import time
import traceback
import logging

from src.cache_instance import cache
from src.auto_loop import auto_loop
from src.ingest_discovery import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts
from src.sentiment_news import fetch_news_sentiment_scores
from src.sentiment_reddit import fetch_sentiment_scores
from src import dashboard
from src.history import router as history_router
from src.leaderboard import router as leaderboard_router


app = FastAPI(title="MoonWire Signal Engine")
app.include_router(dashboard.router)
app.include_router(leaderboard_router)
app.include_router(history_router)

logging.basicConfig(level=logging.INFO)

def safe_auto_loop():
    print(">>> [Thread] auto_loop() starting...")
    try:
        auto_loop()
    except Exception:
        print("!!! auto_loop() crashed:")
        traceback.print_exc()

def hold_forever():
    print(">>> [Main Thread] Blocking indefinitely to keep service alive.")
    while True:
        print(">>> [Main Thread] Still holding...")
        time.sleep(300)

@app.on_event("startup")
async def startup_event():
    print(">>> [Startup] FastAPI server starting...")
    thread = Thread(target=safe_auto_loop, daemon=False)
    thread.start()
    hold_thread = Thread(target=hold_forever, daemon=False)
    hold_thread.start()

@app.get("/")
def root():
    return {"status": "MoonWire Signal Engine is online."}

@app.post("/ingest")
async def ingest(background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest_market_data)
    return {"message": "Ingest started."}

@app.post("/generate_signals")
async def generate(background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_signals)
    return {"message": "Signal generation started."}

@app.post("/dispatch_alerts")
async def dispatch(background_tasks: BackgroundTasks):
    background_tasks.add_task(dispatch_alerts)
    return {"message": "Alert dispatch started."}

@app.post("/test-alert")
async def test_alert(background_tasks: BackgroundTasks):
    test_signal = {
        "asset": "TEST",
        "price_change": 12.5,
        "volume": 50000000,
        "sentiment": 0.2,
        "confidence_score": 0.78,
        "confidence_label": "High Confidence",
        "timestamp": datetime.utcnow().isoformat()
    }
    background_tasks.add_task(dispatch_alerts, asset="TEST", signal=test_signal, cache=cache)
    return {"message": "Test alert sent to dispatcher."}

@app.get("/test-sentiment")
def test_sentiment():
    sentiment = fetch_sentiment_scores()
    return sentiment

@app.get("/test-news-sentiment")
def test_news_sentiment():
    sentiment = fetch_news_sentiment_scores()
    return sentiment