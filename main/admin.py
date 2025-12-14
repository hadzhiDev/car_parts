from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Warehouse, Country, Brand, Product, Arrival, ArrivalProduct, CurrencyRate


@admin.register(ArrivalProduct)
class ArrivalProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article_number', 'arrival__date', 'quantity', 'cost_price', 
                    'brand__name', 'suits_for')
    list_display_links = ('name', 'article_number')
    search_fields = ('name', 'article_number')
    list_filter = ('arrival__date', 'brand__name',)


class ArrivalProductInline(admin.TabularInline):
    model = ArrivalProduct
    extra = 5

    fields = ('name', 'article_number', 'quantity', 'cost_price', 'brand', 'suits_for')
    raw_id_fields = ('brand',)
    can_delete = False


@admin.register(Arrival)
class ArrivalAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse__name', 'date', 'country_of_origin', 'comment')
    list_filter = ('warehouse__name', 'date')
    search_fields = ('id', 'warehouse__name')
    inlines = [ArrivalProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('article_number', 'name', 'brand__name', 'country_of_origin', 'warehouse',  
                    'quantity', 'selling_price', 'suits_for')
    list_display_links = ('article_number', 'name')
    search_fields = ('name', 'article_number')
    list_filter = ('warehouse__name', 'brand__name', 'country_of_origin__name')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'flag_image_display')
    search_fields = ('name',)

    @admin.display(description='Флаг')
    def flag_image_display(self, obj):
        if obj.flag_image:
            return mark_safe(f'<img src="{obj.flag_image.url}" width="100" height="60" />')
        return "-"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_display')
    search_fields = ('name',)

    @admin.display(description='Логотип')
    def logo_display(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="100" height="70" />')
        return "-"
    

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency_code', 'rate_to_usd', 'last_updated')
    search_fields = ('currency_code',)
    list_filter = ('last_updated',)