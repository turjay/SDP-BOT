class SignalPool:
    """
    A class to manage and combine trading signals from various strategies.

    This class allows the addition, removal, and combination of trading signals
    from multiple strategies, and provides a final decision based on weighted majority.
    """

    def __init__(self):
        """
        Initializes the SignalPool with an empty dictionary to store signals.

        Signals are stored in a dictionary where the key is the signal name,
        and the value contains the signal's decision ('buy', 'sell', 'hold') and its weight.
        """
        self.signals = {}

    def add_signal(self, name: str, value: str, weight: int = 1):
        """
        Adds or updates a signal in the pool with a given weight.

        Args:
            name (str): The name of the signal (e.g., 'macd', 'rsi').
            value (str): The value of the signal ('buy', 'sell', 'hold').
            weight (int, optional): The weight of the signal in the decision-making process (default is 1).
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

        Returns:
            str: The combined signal decision ('buy', 'sell', 'hold').
        """
        buy_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'buy')
        sell_weight = sum(sig['weight'] for sig in self.signals.values() if sig['value'] == 'sell')

        # Determine the final decision based on the weights
        if buy_weight > sell_weight:
            return 'buy'
        elif sell_weight > buy_weight:
            return 'sell'
        else:
            return 'hold'

    def reset(self):
        """
        Clears all signals from the pool.

        This method is useful for resetting the pool before adding new signals in the next iteration.
        """
        self.signals.clear()