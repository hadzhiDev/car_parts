from django.contrib import admin

from .models import Sale, SaleItem, Client





class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    raw_id_fields = ('product',)

 
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_date', 'client__full_name')
    list_filter = ('sale_date', 'client__full_name')
    search_fields = ('id', 'client__full_name')
    inlines = [SaleItemInline]
    raw_id_fields = ('client',)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale__id', 'product__name', 'quantity', 'sale_price')
    search_fields = ('sale__id', 'product__name')
    list_filter = ('sale__sale_date', 'product__brand__name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'balance', 'address')
    search_fields = ('full_name', 'phone_number')