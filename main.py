from fastapi import FastAPI, BackgroundTasks
from src.ingest import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts
from src.cache import SignalCache

app = FastAPI(title="MoonWire Signal Engine")

cache = SignalCache()

@app.on_event("startup")
async def startup_event():
    print("MoonWire Signal Engine is online.")

@app.post("/ingest")
async def ingest(background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest_market_data)
    return {"message": "Ingest started."}

@app.post("/generate_signals")
async def generate(background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_signals, cache)
    return {"message": "Signal generation started."}

@app.post("/dispatch_alerts")
async def dispatch(background_tasks: BackgroundTasks):
    background_tasks.add_task(dispatch_alerts, cache)
    return {"message": "Alert dispatch started."}