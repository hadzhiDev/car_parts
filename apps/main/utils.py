from decimal import Decimal

from .models import CurrencyRate

def convert_from_usd(amount):
    selected_currency = CurrencyRate.objects.filter(selected=True).first()
    if amount is None:
        return None
    if not selected_currency:
        return f"{amount} USD"
    return f"{(amount / selected_currency.rate_to_usd).quantize(Decimal('0.01'))} {selected_currency.currency_code}"

