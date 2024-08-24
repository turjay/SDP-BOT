class SignalPool:
    """
    A class to manage and combine trading signals from various strategies.

    Çeşitli stratejilerden gelen ticaret sinyallerini yönetmek ve birleştirmek için bir sınıf.
    """

    def __init__(self):
        """
        Initializes the SignalPool with an empty dictionary to store signals.

        SignalPool'u sinyalleri saklamak için boş bir sözlük ile başlatır.
        """
        self.signals = {}

    def add_signal(self, name, value, weight=1):
        """
        Adds or updates a signal in the pool with a given weight.

        Sinyal havuzuna verilen ağırlıkla yeni bir sinyal ekler veya mevcut sinyali günceller.

        Args:
            name (str): The name of the signal (e.g., 'macd', 'rsi').
            value (str): The value of the signal ('buy', 'sell', 'hold').
            weight (int, optional): The weight of the signal in the decision-making process (default is 1).

        Returns:
            None
        """
        self.signals[name] = {'value': value, 'weight': weight}

    def remove_signal(self, name):
        """
        Removes a signal from the pool.

        Sinyal havuzundan bir sinyali kaldırır.

        Args:
            name (str): The name of the signal to remove.

        Returns:
            None
        """
        if name in self.signals:
            del self.signals[name]

    def get_combined_signal(self):
        """
        Combines all signals in the pool to make a decision based on weighted majority.

        Sinyal havuzundaki tüm sinyalleri birleştirerek ağırlıklı çoğunluğa dayalı bir karar alır.

        The function calculates the total weight of 'buy' and 'sell' signals.
        The decision is made by comparing the total weights:
        - Returns 'buy' if buy signals have a higher total weight.
        - Returns 'sell' if sell signals have a higher total weight.
        - Returns 'hold' if the weights are equal.

        Fonksiyon, 'buy' ve 'sell' sinyallerinin toplam ağırlığını hesaplar.
        Karar, toplam ağırlıkların karşılaştırılmasıyla alınır:
        - Eğer 'buy' sinyalleri daha yüksek ağırlığa sahipse 'buy' döndürür.
        - Eğer 'sell' sinyalleri daha yüksek ağırlığa sahipse 'sell' döndürür.
        - Eğer ağırlıklar eşitse 'hold' döndürür.

        Returns:
            str: The combined signal decision ('buy', 'sell', 'hold').
        """
        buy_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'buy')
        sell_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'sell')

        if buy_weight > sell_weight:
            return 'buy'
        elif sell_weight > buy_weight:
            return 'sell'
        else:
            return 'hold'

    def reset(self):
        """
        Clears all signals from the pool.

        Sinyal havuzundaki tüm sinyalleri temizler.

        This function is useful to reset the pool after a trading decision has been made.

        Bu fonksiyon, bir ticaret kararı alındıktan sonra havuzu sıfırlamak için kullanışlıdır.

        Returns:
            None
        """
        self.signals.clear()
