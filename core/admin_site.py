from django.contrib.admin import AdminSite
from apps.main.models import CurrencyRate

class MyAdminSite(AdminSite):
    site_header = "Car Parts Admin"

    def each_context(self, request):
        context = super().each_context(request)
        context['currencies'] = CurrencyRate.objects.all()
        context['current_currency'] = request.session.get('admin_currency', 'USD')
        return context


admin_site = MyAdminSite()