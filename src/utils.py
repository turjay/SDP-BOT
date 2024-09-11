from decimal import Decimal, ROUND_DOWN

<<<<<<< HEAD
def format_quantity(quantity: float, precision: int = 8) -> Decimal:
    """
    Formats a given quantity to a specified precision.

    Args:
        quantity (float): The quantity to be formatted.
=======
def format_quantity(quantity, precision=8):
    """
    Formats a given quantity to a specified precision.

    Verilen miktarı belirli bir hassasiyete göre formatlar.

    This function takes a quantity and formats it to a specified number of decimal places,
    rounding down if necessary. It is useful in financial applications where precision is critical.

    Bu fonksiyon, bir miktarı belirli bir ondalık basamağa kadar formatlar ve 
    gerekirse aşağı yuvarlar. Finansal uygulamalarda, hassasiyetin kritik olduğu durumlarda kullanışlıdır.

    Args:
        quantity (float or str): The quantity to be formatted.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
        precision (int, optional): The number of decimal places to format to (default is 8).

    Returns:
        Decimal: The formatted quantity as a Decimal object.
    """
<<<<<<< HEAD
    # Ensure the quantity is formatted to the specified number of decimal places, rounding down
    return Decimal(quantity).quantize(Decimal(f'1e-{precision}'), rounding=ROUND_DOWN)

def check_balance(symbol: str, required_amount: float, balances: list) -> bool:
    """
    Checks if there is sufficient balance for a given asset symbol.

    Args:
        symbol (str): The symbol (e.g., 'BTC', 'TRY') to check the balance for.
        required_amount (float): The amount required to complete a transaction.
        balances (list of dict): A list of dictionaries containing balance information for each asset.
=======
    return Decimal(quantity).quantize(Decimal('1e-{0}'.format(precision)), rounding=ROUND_DOWN)

def check_balance(symbol, required_amount, balances):
    """
    Checks if there is sufficient balance for a given symbol.

    Belirli bir sembolde yeterli bakiye olup olmadığını kontrol eder.

    This function iterates through a list of balances to find the balance for the specified symbol.
    If the free balance for that symbol is greater than or equal to the required amount, it returns True.
    Otherwise, it returns False.

    Bu fonksiyon, belirtilen sembol için bakiyeyi bulmak amacıyla bakiye listesini tarar. 
    Eğer o sembol için serbest bakiye, gerekli miktardan büyük veya eşitse True döndürür.
    Aksi takdirde False döndürür.

    Args:
        symbol (str): The symbol (e.g., 'BTC', 'TRY') to check the balance for.
        required_amount (float): The amount required.
        balances (list of dict): A list of dictionaries containing balance information.
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de

    Returns:
        bool: True if the required balance is available, False otherwise.
    """
<<<<<<< HEAD
    # Iterate through the balance list and find the balance for the given symbol
    for item in balances:
        if item['asset'] == symbol:
            free_balance = float(item['free'])  # Get the free (available) balance for the symbol
            return free_balance >= required_amount  # Check if the balance is sufficient
    return False  # Return False if the symbol is not found or balance is insufficient
=======
    for item in balances:
        if item['asset'] == symbol:
            free_balance = float(item['free'])  # Convert balance to float / Bakiyeyi float'a dönüştür
            if free_balance >= required_amount:
                return True
    return False
>>>>>>> 9bd2ee40ba510e2e19da446929feb5e2ad1c44de
