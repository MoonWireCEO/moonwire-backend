class SignalCache:
    def __init__(self):
        self._store = {}

    def get_signal(self, key):
        return self._store.get(f"{key}_signal", {})

    def set_signal(self, key, value):
        self._store[f"{key}_signal"] = value

    def get_history(self, key):
        return self._store.get(f"{key}_history", [])

    def set_history(self, key, value):
        self._store.setdefault(f"{key}_history", []).append(value)

    def keys(self):
        return self._store.keys()