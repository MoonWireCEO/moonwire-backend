import redis
import json

class SignalCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set_signal(self, key, value):
        self.client.set(key, json.dumps(value))

    def get_signal(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete_signal(self, key):
        self.client.delete(key)