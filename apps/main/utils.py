from django.utils.dateparse import parse_date
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

from .models import CurrencyRate


def normalize_name(name: str) -> str:
    if not name:
        return ''
    return ' '.join(name.strip().upper().split())


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


def parse_admin_date(value):
    """
    Supports:
    - YYYY-MM-DD (ISO)
    - DD.MM.YYYY (admin UI)
    """
    if not value:
        return None

    date = parse_date(value)
    if date:
        return date

    try:
        return datetime.strptime(value, '%d.%m.%Y').date()
    except ValueError:
        return None