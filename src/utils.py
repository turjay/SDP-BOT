from decimal import Decimal, ROUND_DOWN

# Miktarı belirli bir hassasiyetle formatlayan fonksiyon
def format_quantity(quantity, precision=8):
    return Decimal(quantity).quantize(Decimal('1e-{0}'.format(precision)), rounding=ROUND_DOWN)

# Bakiye kontrolü yapan fonksiyon; belirli bir sembolde yeterli bakiye olup olmadığını kontrol eder
def check_balance(symbol, required_amount, balances):
    for item in balances:
        if item['asset'] == symbol:
            free_balance = float(item['free'])
            if free_balance >= required_amount:
                return True
    return False