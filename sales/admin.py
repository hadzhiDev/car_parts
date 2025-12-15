from django.contrib import admin

from .models import Sale, SaleItem, Client, Payment


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    raw_id_fields = ('product',)

 
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_date', 'client__full_name', 'total_amount')
    list_filter = ('sale_date', 'client__full_name')
    search_fields = ('id', 'client__full_name')
    inlines = [SaleItemInline]
    raw_id_fields = ('client',)

    @admin.display(description='Общая сумма')
    def total_amount(self, obj):
        return obj.total_amount


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale__id', 'product__name', 'quantity', 'sale_price')
    search_fields = ('sale__id', 'product__name')
    list_filter = ('sale__sale_date', 'product__brand__name',)


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