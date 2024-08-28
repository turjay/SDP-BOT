from decimal import Decimal, ROUND_DOWN

def format_quantity(quantity: float, precision: int = 8) -> Decimal:
    """
    Formats a given quantity to a specified precision.

    Args:
        quantity (float): The quantity to be formatted.
        precision (int, optional): The number of decimal places to format to (default is 8).

    Returns:
        Decimal: The formatted quantity as a Decimal object.
    """
    # Ensure the quantity is formatted to the specified number of decimal places, rounding down
    return Decimal(quantity).quantize(Decimal(f'1e-{precision}'), rounding=ROUND_DOWN)

def check_balance(symbol: str, required_amount: float, balances: list) -> bool:
    """
    Checks if there is sufficient balance for a given asset symbol.

    Args:
        symbol (str): The symbol (e.g., 'BTC', 'TRY') to check the balance for.
        required_amount (float): The amount required to complete a transaction.
        balances (list of dict): A list of dictionaries containing balance information for each asset.

    Returns:
        bool: True if the required balance is available, False otherwise.
    """
    # Iterate through the balance list and find the balance for the given symbol
    for item in balances:
        if item['asset'] == symbol:
            free_balance = float(item['free'])  # Get the free (available) balance for the symbol
            return free_balance >= required_amount  # Check if the balance is sufficient
    return False  # Return False if the symbol is not found or balance is insufficient