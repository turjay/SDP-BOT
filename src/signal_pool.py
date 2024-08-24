class SignalPool:
    def __init__(self):
        self.signals = {}

    # Sinyal havuzuna yeni bir sinyal ekleyen veya güncelleyen fonksiyon
    def add_signal(self, name, value, weight=1):
        """Add or update a signal in the pool with a given weight."""
        self.signals[name] = {'value': value, 'weight': weight}

    # Sinyal havuzundan bir sinyali kaldıran fonksiyon
    def remove_signal(self, name):
        """Remove a signal from the pool."""
        if name in self.signals:
            del self.signals[name]

    # Tüm sinyalleri birleştirerek bir karar alan fonksiyon
    def get_combined_signal(self):
        """Combine all signals to make a decision based on weighted majority."""
        buy_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'buy')
        sell_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'sell')

        if buy_weight > sell_weight:
            return 'buy'
        elif sell_weight > buy_weight:
            return 'sell'
        else:
            return 'hold'

    # Tüm sinyalleri temizleyen fonksiyon
    def reset(self):
        """Clear all signals."""
        self.signals.clear()