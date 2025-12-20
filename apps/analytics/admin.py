# analytics/admin.py
from django.urls import path
from django.contrib import admin
from .views import analytics_dashboard, sales_report, inventory_report, profit_report

from .models import AnalyticsReport


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    """Admin interface for analytics"""
    
    change_list_template = 'admin/analytics_change_list.html'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Redirect to analytics dashboard
        return analytics_dashboard(request)
    
    def get_urls(self):
        # Use self.admin_site.admin_view() to wrap your custom views
        urls = super().get_urls()
        custom_urls = [
            path('sales/', self.admin_site.admin_view(sales_report), name='sales_report'),
            path('inventory/', self.admin_site.admin_view(inventory_report), name='inventory_report'),
            path('profit/', self.admin_site.admin_view(profit_report), name='profit_report'),
        ]
        return custom_urls + urls