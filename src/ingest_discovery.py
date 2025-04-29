import requests

def ingest_market_data(cache):
    print("🛰️ Ingesting market data...")

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for asset in data:
            symbol = asset["symbol"].upper()
            cache.set_signal(symbol, {
                "price_now": asset["current_price"],
                "price_change_24h": asset["price_change_percentage_24h"],
                "volume_now": asset["total_volume"],
                "market_cap": asset["market_cap"]
            })

        print("✅ Market data ingested.")

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("⚠️ CoinGecko rate limit hit (429). Skipping ingest this cycle.")
        else:
            print(f"❌ HTTP error during ingest: {str(e)}")

    except Exception as e:
        print(f"❌ General error during ingest: {str(e)}")