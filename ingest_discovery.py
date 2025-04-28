import requests
from src.logger import log

def ingest_market_data(cache):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        for asset in data:
            symbol = asset['symbol'].upper()
            cache.set_signal(symbol, {
                'price_now': asset['current_price'],
                'volume_now': asset['total_volume'],
                'price_change_24h': asset['price_change_percentage_24h'],
                'market_cap': asset['market_cap']
            })
            log(f"[Discovery Ingested] {symbol}: price ${asset['current_price']}, vol {asset['total_volume']}")
    except Exception as e:
        log(f"[ERROR] Discovery Ingest failed: {str(e)}")