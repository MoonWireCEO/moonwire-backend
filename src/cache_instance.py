class SignalCache:
    def __init__(self):
        self.signals = {}
        self.sentiment_scores = {}

    def get_signals(self, key):
        return self.signals.get(key, [])

    def set_signal(self, key, signals):
        self.signals[key] = signals

    def store_signal(self, asset, signal):
        key = f"{asset}_signals"
        if key not in self.signals:
            self.signals[key] = []
        self.signals[key].append(signal)

    def get_sentiment(self, asset):
        return self.sentiment_scores.get(asset, 0.0)

    def set_sentiment(self, asset, score):
        self.sentiment_scores[asset] = score