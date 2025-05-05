class SignalCache:
    def __init__(self):
        self._store = {}

    def get_signal(self, key):
        return self._store.get(key, [])

    def set_signal(self, key, value):
        self._store[key] = value

    def clear(self):
        self._store.clear()

    def add_to_history(self, asset, signal):
        key = f"{asset}_history"
        history = self._store.get(key, [])
        history.append(signal)
        self._store[key] = history