from apps.main.models import CurrencyRate

def admin_currency(request):
    return {
        "admin_currencies": CurrencyRate.objects.all(),
        "admin_currency_selected": CurrencyRate.objects.filter(selected=True).first(),
    }
