from django.contrib import admin
from django.http import HttpResponse
from rangefilter.filters import DateTimeRangeFilter, DateRangeFilterBuilder

from .models import Sale, SaleItem, Client, Payment
from apps.main.utils import convert_from_usd
from .filters import SaleDateRangeFilter

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter



@admin.action(description='Экспорт выбранных товаров продажи в Excel')
def export_sale_items_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Товары продажи"

    headers = [
        "Продажа ID",
        "Дата продажи",
        "Клиент",
        "Товар",
        "Артикул",
        "Количество",
        "Цена продажи",
        "Сумма",
    ]

    ws.append(headers)

    # ===== Styles =====
    header_font = Font(bold=True)
    center = Alignment(horizontal='center', vertical='center')
    left = Alignment(horizontal='left', vertical='center')

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )

    # ===== Header style =====
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.alignment = center
        cell.border = thin_border

    # ===== Data =====
    for item in queryset.select_related('sale', 'sale__client', 'product'):
        ws.append([
            item.sale.id,
            item.sale.sale_date.strftime('%Y-%m-%d %H:%M'),
            item.sale.client.full_name,
            item.product.name,
            item.product.article_number if hasattr(item.product, 'article_number') else '',
            item.quantity,
            float(item.sale_price),
            float(item.total_cost),
        ])

    # ===== Body styles + borders =====
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for cell in row:
            cell.border = thin_border
            cell.alignment = left if cell.column in [3, 4] else center

    # ===== Auto-fit column width (fit content) =====
    for column_cells in ws.columns:
        max_length = 0
        col_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[col_letter].width = max_length + 2

    # ===== Response =====
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="sale_items.xlsx"'

    wb.save(response)
    return response



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
    autocomplete_fields = ('client',)

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
    list_filter = ('sale__sale_date', 'product__brand__name', 
                   ('sale__sale_date', DateRangeFilterBuilder()),
    )
    actions = (export_sale_items_to_excel,)

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