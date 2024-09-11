class SignalPool:
    """
    A class to manage and combine trading signals from various strategies.

<<<<<<< HEAD
    This class allows the addition, removal, and combination of trading signals
    from multiple strategies, and provides a final decision based on weighted majority.
=======
    Çeşitli stratejilerden gelen ticaret sinyallerini yönetmek ve birleştirmek için bir sınıf.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
    """

    def __init__(self):
        """
        Initializes the SignalPool with an empty dictionary to store signals.

<<<<<<< HEAD
        Signals are stored in a dictionary where the key is the signal name,
        and the value contains the signal's decision ('buy', 'sell', 'hold') and its weight.
        """
        self.signals = {}

    def add_signal(self, name: str, value: str, weight: int = 1):
        """
        Adds or updates a signal in the pool with a given weight.

=======
        SignalPool'u sinyalleri saklamak için boş bir sözlük ile başlatır.
        """
        self.signals = {}

    def add_signal(self, name, value, weight=1):
        """
        Adds or updates a signal in the pool with a given weight.

        Sinyal havuzuna verilen ağırlıkla yeni bir sinyal ekler veya mevcut sinyali günceller.

>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
        Args:
            name (str): The name of the signal (e.g., 'macd', 'rsi').
            value (str): The value of the signal ('buy', 'sell', 'hold').
            weight (int, optional): The weight of the signal in the decision-making process (default is 1).
<<<<<<< HEAD
        """
        # Add or update the signal in the dictionary
        self.signals[name] = {'value': value, 'weight': weight}

    def remove_signal(self, name: str):
        """
        Removes a signal from the pool by its name.

        Args:
            name (str): The name of the signal to remove.
        """
        # Check if the signal exists and remove it
        if name in self.signals:
            del self.signals[name]

    def get_combined_signal(self) -> str:
        """
        Combines all signals in the pool to make a decision based on weighted majority.

        This method calculates the total weight for each decision ('buy', 'sell') and returns the
        decision with the highest weight. In case of a tie, 'hold' is returned.
=======

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
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de

        Returns:
            str: The combined signal decision ('buy', 'sell', 'hold').
        """
        buy_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'buy')
        sell_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'sell')

<<<<<<< HEAD
        # Determine the final decision based on the weights
=======
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
        if buy_weight > sell_weight:
            return 'buy'
        elif sell_weight > buy_weight:
            return 'sell'
        else:
            return 'hold'

    def reset(self):
        """
        Clears all signals from the pool.

<<<<<<< HEAD
        This method is useful for resetting the pool before adding new signals in the next iteration.
        """
        self.signals.clear()
=======
        Sinyal havuzundaki tüm sinyalleri temizler.

        This function is useful to reset the pool after a trading decision has been made.

        Bu fonksiyon, bir ticaret kararı alındıktan sonra havuzu sıfırlamak için kullanışlıdır.

        Returns:
            None
        """
        self.signals.clear()
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
