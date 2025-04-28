# src/auto_loop.py

import time
from src.ingest_discovery import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts

def auto_loop(cache, interval=600):
    """
    Background loop to run ingestion, signal generation, and dispatch every 'interval' seconds.
    Default interval = 300 seconds (5 minutes).
    """
    print("MoonWire Auto-Loop Started...")
    while True:
        try:
            print("Running Ingest...")
            ingest_market_data(cache)
            print("Running Signal Generation...")
            generate_signals(cache)
            print("Running Dispatch...")
            dispatch_alerts(cache)
            print(f"Cycle complete. Sleeping {interval} seconds...\n")
        except Exception as e:
            print(f"Error in auto-loop: {str(e)}")
        time.sleep(interval)
