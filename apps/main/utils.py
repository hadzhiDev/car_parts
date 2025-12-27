from decimal import Decimal, ROUND_HALF_UP

from .models import CurrencyRate


def convert_from_usd(amount):
    if amount is None:
        return None

    selected_currency = CurrencyRate.objects.filter(selected=True).first()

    if not selected_currency:
        return f"{amount} USD"

    converted = (
        Decimal(amount) * selected_currency.rate_to_usd
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return f"{converted} {selected_currency.currency_code}"

