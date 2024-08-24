from decimal import Decimal, ROUND_DOWN

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
        precision (int, optional): The number of decimal places to format to (default is 8).

    Returns:
        Decimal: The formatted quantity as a Decimal object.
    """
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

    Returns:
        bool: True if the required balance is available, False otherwise.
    """
    for item in balances:
        if item['asset'] == symbol:
            free_balance = float(item['free'])  # Convert balance to float / Bakiyeyi float'a dönüştür
            if free_balance >= required_amount:
                return True
    return False