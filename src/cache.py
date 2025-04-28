# src/cache.py

class SignalCache:
    def __init__(self):
        # Use a simple Python dictionary instead of Redis for now
        self.cache = {}

    def set_signal(self, key, value):
        # Set a value in the in-memory cache
        self.cache[key] = value

    def get_signal(self, key):
        # Retrieve a value from the cache
        return self.cache.get(key, None)

    def delete_signal(self, key):
        # Delete a value from the cache
        if key in self.cache:
            del self.cache[key]