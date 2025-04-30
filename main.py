from fastapi import FastAPI, BackgroundTasks
from src.ingest_discovery import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts
from src.cache import SignalCache
from threading import Thread
from src.auto_loop import auto_loop
import traceback

app = FastAPI(title="MoonWire Signal Engine")
cache = SignalCache()

def safe_auto_loop():
    print(">>> auto_loop() thread starting...")
    try:
        auto_loop(cache)
    except Exception as e:
        print("!!! auto_loop() crashed with exception:")
        traceback.print_exc()

@app.on_event("startup")
async def startup_event():
    print(">>> FastAPI startup triggered.")
    thread = Thread(target=safe_auto_loop, daemon=True)
    thread.start()

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