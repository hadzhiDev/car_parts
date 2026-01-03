from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CurrencyRate, Product


def product_autofill(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return JsonResponse({
        "name": product.name,
        "article_number": product.article_number,
        "cost_price": str(product.cost_price or ""),
        "brand_id": product.brand_id,
        "brand_name": product.brand.name,
    })



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