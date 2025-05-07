# src/twitter_ingestor.py

import subprocess
import json
from datetime import datetime, timedelta

def fetch_tweets(keyword, limit=20):
    since = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    query = f'{keyword} since:{since}'
    cmd = ['snscrape', '--jsonl', '--max-results', str(limit), 'twitter-search', query]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        tweets = [json.loads(line) for line in result.stdout.splitlines()]
        return [t['content'] for t in tweets]
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []