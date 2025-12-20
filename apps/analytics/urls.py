# analytics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/sales-report/', views.sales_report, name='sales_report'),
    path('analytics/inventory-report/', views.inventory_report, name='inventory_report'),
    path('analytics/profit-report/', views.profit_report, name='profit_report'),
]