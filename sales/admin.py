from django.contrib import admin

from .models import Sale, SaleItem, Client, Payment
from main.utils import convert_from_usd


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    autocomplete_fields = ('product',)
    readonly_fields = ('row_total',)
    fields = (
        'product',
        'quantity',
        'sale_price',
        'row_total',
    )
    def row_total(self, obj):
        print('obj.total_cost: ', obj.total_cost)
        return "—"
    row_total.short_description = "Итого"

 
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_date', 'client__full_name', 'total_amount')
    list_display_links = ('id', 'sale_date')
    list_filter = ('sale_date', 'client__full_name')
    search_fields = ('id', 'client__full_name')
    inlines = [SaleItemInline]
    raw_id_fields = ('client',)

    @admin.display(description='Общая сумма')
    def total_amount(self, obj):
        return convert_from_usd(obj.total_amount)
    
    class Media:
        js = ('admin/inline_totals.js',)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale__id', 'product__name', 'show_quantity', 'sale_price_converted', 'total_cost')
    list_display_links = ('sale__id', 'product__name')
    search_fields = ('sale__id', 'product__name')
    list_filter = ('sale__sale_date', 'product__brand__name',)

    @admin.display(description='Количество')
    def show_quantity(self, obj):
        return f"{obj.quantity} шт."

    @admin.display(description='Цена продажи')
    def sale_price_converted(self, obj):
        return convert_from_usd(obj.sale_price)

    @admin.display(description='Итоговая стоимость')
    def total_cost(self, obj):
        return convert_from_usd(obj.total_cost)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'balance', 'address')
    search_fields = ('full_name', 'phone_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client__full_name', 'amount', 'payment_date')
    search_fields = ('client__full_name',)
    list_filter = ('payment_date',)
    autocomplete_fields = ('client',)

    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_change_permission(request, obj)