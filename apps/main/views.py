from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CurrencyRate


@staff_member_required
@require_POST
def set_admin_currency(request):
    currency_code = request.POST.get("currency")

    CurrencyRate.objects.update(selected=False)

    if currency_code != "USD":
        currency = get_object_or_404(
            CurrencyRate,
            currency_code=currency_code
        )
        currency.selected = True
        currency.save(update_fields=["selected"])

    return JsonResponse({"status": "ok"})