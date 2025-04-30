# src/auto_loop.py

import time
import traceback
from datetime import datetime
from src.ingest_discovery import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts

def auto_loop(cache, interval=600):
    print("✅ MoonWire Auto-Loop Started...")

    while True:
        cycle_start = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        print(f"--- Starting New Cycle @ {cycle_start} UTC ---")

        try:
            print("🔁 Running Ingest...")
            ingest_market_data(cache)

            print("🧠 Running Signal Generation...")
            generate_signals(cache)

            print("📣 Running Dispatch...")
            dispatch_alerts(cache)

        except Exception as e:
            print(f"❌ Exception in auto-loop: {str(e)}")
            traceback.print_exc()

        finally:
            print(f"⏳ Sleeping for {interval} seconds...\n")
            time.sleep(interval)

