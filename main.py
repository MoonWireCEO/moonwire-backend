from fastapi import FastAPI, BackgroundTasks
from src.ingest_discovery import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts
from src.cache import SignalCache
from threading import Thread
from src.auto_loop import auto_loop
import asyncio
import traceback

app = FastAPI(title="MoonWire Signal Engine")
cache = SignalCache()

def safe_auto_loop():
    print(">>> [Thread] auto_loop() starting...")
    try:
        auto_loop(cache)
    except Exception as e:
        print("!!! auto_loop() crashed:")
        traceback.print_exc()

async def _keep_alive_with_heartbeat():
    while True:
        print(">>> [Heartbeat] FastAPI server alive.")
        await asyncio.sleep(300)  # Log every 5 minutes

@app.on_event("startup")
async def startup_event():
    print(">>> [Startup] FastAPI server starting...")
    # Launch the background auto_loop
    thread = Thread(target=safe_auto_loop, daemon=False)
    thread.start()
    # Launch async heartbeat task to keep event loop active
    asyncio.create_task(_keep_alive_with_heartbeat())

@app.get("/")
def root():
    return {"status": "MoonWire Signal Engine is online."}

@app.post("/ingest")
async def ingest(background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest_market_data, cache)
    return {"message": "Ingest started."}

@app.post("/generate_signals")
async def generate(background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_signals, cache)
    return {"message": "Signal generation started."}

@app.post("/dispatch_alerts")
async def dispatch(background_tasks: BackgroundTasks):
    background_tasks.add_task(dispatch_alerts, cache)
    return {"message": "Alert dispatch started."}