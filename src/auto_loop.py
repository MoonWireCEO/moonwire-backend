# src/auto_loop.py

import time
from src.ingest_discovery import ingest_market_data
from src.signal_generator import generate_signals
from src.dispatcher import dispatch_alerts
from src.cache_sentiment import update_sentiment_cache

def auto_loop(interval=600):
    print("✅ MoonWire Auto-Loop Started...")

    while True:
        try:
            print("💬 Updating sentiment...")
            update_sentiment_cache()

            print("🔁 Running Ingest...")
            ingest_market_data()

            print("🧠 Running Signal Generation...")
            generate_signals()

            print("📣 Running Dispatch...")
            dispatch_alerts()

            print(f"✅ Cycle complete. Sleeping for {interval} seconds...\n")

        except Exception as e:
            print(f"❌ Error in auto-loop: {str(e)}")

        print(f"⏳ Sleeping for {interval} seconds...\n")
        time.sleep(interval)
