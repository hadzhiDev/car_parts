from decimal import Decimal
# from django.conf import settings

from .models import CurrencyRate

def convert_from_usd(amount):
    selected_currency = CurrencyRate.objects.filter(selected=True).first()
    print('selected_currency: ', selected_currency, amount)
    if amount is None:
        return None
    if not selected_currency:
        return f"{amount} USD"
    return f"{(amount / selected_currency.rate_to_usd).quantize(Decimal('0.01'))} {selected_currency.currency_code}"


# class CurrencyAdminMixin:
#     def get_currency(self, request):
#         print('code: ', request.session.get('admin_currency'))
#         code = request.session.get('admin_currency', 'USD')
#         try:
#             return CurrencyRate.objects.get(currency_code=code)
#         except CurrencyRate.DoesNotExist:
#             return None

#     def format_money(self, request, amount):
#         currency = self.get_currency(request)
#         # print(currency)
#         if not currency or amount is None:
#             return amount
#         converted = amount / currency.rate_to_usd
#         return f"{converted:.2f} {currency.currency_code}"
