from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Warehouse, Country, Brand, Product, Arrival, ArrivalProduct, CurrencyRate
from .utils import convert_from_usd
# from core.admin_site import admin_site


@admin.register(ArrivalProduct)
class ArrivalProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article_number', 'arrival__date', 'show_quantity', 'cost_price_converted', 
                    'total_cost_converted', 'brand__name', 'suits_for')
    list_display_links = ('name', 'article_number')
    search_fields = ('name', 'article_number')
    list_filter = ('arrival__date', 'brand__name',)

    def cost_price_converted(self, obj):
        return convert_from_usd(obj.cost_price)
    cost_price_converted.short_description = "Себестоимость"

    def total_cost_converted(self, obj):
        return convert_from_usd(obj.total_cost)
    total_cost_converted.short_description = "Общая стоимость"

    @admin.display(description='Количество')
    def show_quantity(self, obj):
        return f"{obj.quantity} шт."


class ArrivalProductInline(admin.TabularInline):
    model = ArrivalProduct
    extra = 5
    
    fields = (
        'name',
        'article_number',
        'quantity',
        'cost_price',
        'row_total',
        'brand',
        'suits_for',
    )
    readonly_fields = ('row_total',)
    autocomplete_fields = ('brand',)
    can_delete = False

    def row_total(self, obj):
        print('obj.total_cost: ', obj.total_cost)
        return "—"
    row_total.short_description = "Итого"



@admin.register(Arrival)
class ArrivalAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'warehouse__name', 'country_of_origin', 'total_amount_converted', 'comment')
    list_display_links = ('id', 'date')
    list_filter = ('warehouse__name', 'date')
    search_fields = ('id', 'warehouse__name')
    inlines = [ArrivalProductInline]

    def total_amount_converted(self, obj):
        return convert_from_usd(obj.total_amount)
    total_amount_converted.short_description = "Общая сумма"

    class Media:
        js = ('admin/arrival_totals.js',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article_number', 'brand__name', 'country_of_origin', 'warehouse',  
                    'show_quantity', 'selling_price', 'suits_for')
    list_display_links = ('name', 'article_number')
    search_fields = ('name', 'article_number')
    list_filter = ('warehouse__name', 'brand__name', 'country_of_origin__name')

    @admin.display(description='Количество')
    def show_quantity(self, obj):
        return f"{obj.quantity} шт."


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
    list_display = ('currency_code', 'rate_to_usd', 'last_updated', 'selected')
    search_fields = ('currency_code',)
    list_filter = ('last_updated',)
    list_editable = ('selected',)
    


# admin_site.register(CurrencyRate, CurrencyRateAdmin)
# admin_site.register(Arrival, ArrivalAdmin)
# admin_site.register(Product, ProductAdmin)
# admin_site.register(ArrivalProduct, ArrivalProductAdmin)
# admin_site.register(Warehouse, WarehouseAdmin)
# admin_site.register(Country, CountryAdmin)
# admin_site.register(Brand, BrandAdmin)