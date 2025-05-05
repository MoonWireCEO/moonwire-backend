class SignalCache:
    def __init__(self):
        self._store = {}

    def get_signal(self, key):
        return self._store.get(key, [])

    def set_signal(self, key, value):
        self._store[key] = value

    def clear(self):
        self._store.clear()

    def keys(self):
        return self._store.keys()