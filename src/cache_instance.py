from src.cache import SignalCache

cache = SignalCache()

class SignalCache:
    def __init__(self):
        self.data = {}

    def store_signal(self, asset, signal):
        key = f"{asset}_signals"
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(signal)

    def get_signals(self, asset):
        key = f"{asset}_signals"
        return self.data.get(key, [])