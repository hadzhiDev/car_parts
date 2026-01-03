from django.contrib.admin import SimpleListFilter


class SoldQuantityFilter(SimpleListFilter):
    title = "Продажи"
    parameter_name = "sold"

    def lookups(self, request, model_admin):
        return (
            ('most', 'Самые продаваемые'),
            ('least', 'Наименее продаваемые'),
            ('none', 'Не продавались'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'most':
            return queryset.filter(active_sold_qty__gt=0).order_by('-active_sold_qty')

        if value == 'least':
            return queryset.order_by('active_sold_qty')

        if value == 'none':
            return queryset.filter(active_sold_qty=0)

        return queryset


class SalePeriodFilter(SimpleListFilter):
    title = "Период продаж"
    parameter_name = "period"

    def lookups(self, request, model_admin):
        return (
            ('today', 'Сегодня'),
            ('week', 'Эта неделя'),
            ('month', 'Этот месяц'),
            ('year', 'Этот год'),
        )

    def queryset(self, request, queryset):
        return queryset 
