from django.contrib.admin import SimpleListFilter
from django.utils.timezone import make_aware
from datetime import datetime


class SaleDateRangeFilter(SimpleListFilter):
    title = 'Дата продажи'
    parameter_name = 'sale_date_range'

    template = 'admin/date_range_filter.html'

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
            end = end.replace(hour=23, minute=59, second=59)

            return queryset.filter(
                sale__sale_date__range=(start, end)
            )

        return queryset
