# src/ingest_discovery.py

import requests
from datetime import datetime

def fetch_from_coinpaprika(asset_id):
    try:
        url = f"https://api.coinpaprika.com/v1/tickers/{asset_id.lower()}-usd"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'price_change_24h': data['quotes']['USD']['percent_change_24h'],
                'volume_now': data['quotes']['USD']['volume_24h']
            }
    except Exception as e:
        print(f"CoinPaprika failed for {asset_id}: {e}")
    return None

def fetch_from_coingecko(asset_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{asset_id.lower()}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'price_change_24h': data['market_data']['price_change_percentage_24h'],
                'volume_now': data['market_data']['total_volume']['usd']
            }
    except Exception as e:
        print(f"CoinGecko failed for {asset_id}: {e}")
    return None

def ingest_market_data(cache):
    print(f"[{datetime.utcnow()}] Ingesting market data...")

    assets = ['bitcoin', 'ethereum', 'solana']  # Add more as needed

    for asset in assets:
        data = fetch_from_coinpaprika(asset)
        if not data:
            print(f"Falling back to CoinGecko for {asset}")
            data = fetch_from_coingecko(asset)

        if data:
            cache.set_signal(asset.upper(), data)
            print(f"Cached data for {asset.upper()}: {data}")
        else:
            print(f"Failed to fetch data for {asset}")
