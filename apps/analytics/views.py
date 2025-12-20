from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper
from django.db.models.functions import TruncMonth, TruncYear
import json
from decimal import Decimal

from main.models import Product, Arrival, Warehouse, Brand, Country, ArrivalProduct
from sales.models import Sale, SaleItem, Client, Payment


@staff_member_required
def analytics_dashboard(request):
    """Main analytics dashboard"""
    
    today = timezone.now().date()
    two_weeks_ago = today - timedelta(days=14)
    thirty_days_ago = today - timedelta(days=30)
    
    recent_sales = SaleItem.objects.filter(
        sale__sale_date__gte=two_weeks_ago
    ).values_list('product_id', flat=True).distinct()
    
    unsold_products = Product.objects.exclude(id__in=recent_sales)
    
    # Inventory summary
    total_inventory_value = sum(
        product.quantity * (product.cost_price or Decimal('0'))
        for product in Product.objects.all()
    )
    
    total_inventory_selling_value = sum(
        product.quantity * (product.selling_price or Decimal('0'))
        for product in Product.objects.all() 
    )
    
    # Sales summary for last 30 days
    recent_sale_items = SaleItem.objects.filter(
        sale__sale_date__gte=thirty_days_ago
    )
    
    recent_sales_summary = recent_sale_items.aggregate(
        total_sales=Count('sale', distinct=True),
        total_amount=Sum(F('quantity') * F('sale_price'))
    )
    
    # Warehouse distribution
    warehouse_stats = []
    for warehouse in Warehouse.objects.all():
        warehouse_products = Product.objects.filter(warehouse=warehouse)
        count = warehouse_products.count()
        total_qty = warehouse_products.aggregate(total=Sum('quantity'))['total'] or 0
        total_value = sum(
            p.quantity * (p.cost_price or Decimal('0')) 
            for p in warehouse_products
        )
        warehouse_stats.append({
            'warehouse': warehouse,
            'count': count,
            'total_qty': total_qty,
            'total_value': total_value
        })
    
    context = {
        'title': 'Панель аналитики',
        'unsold_products': unsold_products[:10],
        'unsold_products_count': unsold_products.count(),
        'total_inventory_value': total_inventory_value,
        'total_inventory_selling_value': total_inventory_selling_value,
        'recent_sales_count': recent_sales_summary['total_sales'] or 0,
        'recent_sales_amount': recent_sales_summary['total_amount'] or 0,
        'warehouse_stats': warehouse_stats,
        'today': today,
        'two_weeks_ago': two_weeks_ago,
        'thirty_days_ago': thirty_days_ago,
    }
    
    return render(request, 'admin/analytics/dashboard.html', context)


@staff_member_required
def sales_report(request):
    """Detailed sales analytics"""
    
    today = timezone.now().date()
    start_date = request.GET.get('start_date', (today - timedelta(days=365)).isoformat())
    end_date = request.GET.get('end_date', today.isoformat())
    
    # Filter sales by date range
    sales = Sale.objects.filter(
        sale_date__date__range=[start_date, end_date]
    )
    
    # Calculate total_amount manually
    total_amount = 0
    for sale in sales:
        total_amount += sale.total_amount
    
    # Monthly sales data - FIXED
    # Instead of annotating with total_amount, calculate manually
    monthly_data = []
    for sale in sales:
        month = sale.sale_date.replace(day=1)
        # Find or create month entry
        found = False
        for entry in monthly_data:
            if entry['month'] == month:
                entry['total_sales'] += 1
                entry['total_amount'] += sale.total_amount
                found = True
                break
        if not found:
            monthly_data.append({
                'month': month,
                'total_sales': 1,
                'total_amount': sale.total_amount
            })
    
    monthly_data.sort(key=lambda x: x['month'])
    
    # Top selling products (this already works correctly)
    top_products = SaleItem.objects.filter(
        sale__sale_date__date__range=[start_date, end_date]
    ).values(
        'product__name', 'product__article_number', 'product__brand__name'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('sale_price'))
    ).order_by('-total_sold')[:20]
    
    # Sales by brand
    sales_by_brand = SaleItem.objects.filter(
        sale__sale_date__date__range=[start_date, end_date]
    ).values(
        'product__brand__name'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('sale_price'))
    ).order_by('-total_revenue')
    
    context = {
        'title': 'Отчет по продажам',
        'monthly_sales': monthly_data,  # Use our calculated data
        'top_products': top_products,
        'sales_by_brand': sales_by_brand,
        'total_sales': sales.count(),
        'total_amount': total_amount,  # Use our calculated total
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'admin/analytics/sales_report.html', context)


@staff_member_required 
def inventory_report(request):
    """Inventory analytics"""
    
    # Slow moving inventory (not sold in 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    recent_sales = SaleItem.objects.filter(
        sale__sale_date__gte=thirty_days_ago
    ).values_list('product_id', flat=True).distinct()
    
    slow_moving = Product.objects.exclude(id__in=recent_sales)
    
    # Inventory by warehouse
    inventory_by_warehouse = []
    for warehouse in Warehouse.objects.all():
        products = Product.objects.filter(warehouse=warehouse)
        total_cost = sum(p.quantity * (p.cost_price or Decimal('0')) for p in products)
        total_selling = sum(p.quantity * (p.selling_price or Decimal('0')) for p in products)
        
        inventory_by_warehouse.append({
            'warehouse': warehouse,
            'product_count': products.count(),
            'total_quantity': products.aggregate(total=Sum('quantity'))['total'] or 0,
            'total_cost_value': total_cost,
            'total_selling_value': total_selling,
            'potential_profit': total_selling - total_cost,
        })
    
    # Inventory by brand
    inventory_by_brand = []
    for brand in Brand.objects.all():
        products = Product.objects.filter(brand=brand)
        if products.exists():
            inventory_by_brand.append({
                'brand': brand,
                'product_count': products.count(),
                'total_quantity': products.aggregate(total=Sum('quantity'))['total'] or 0,
                'total_value': sum(p.quantity * (p.cost_price or Decimal('0')) for p in products),
            })
    
    context = {
        'title': 'Отчет по инвентарю',
        'slow_moving': slow_moving,
        'slow_moving_count': slow_moving.count(),
        'inventory_by_warehouse': inventory_by_warehouse,
        'inventory_by_brand': sorted(inventory_by_brand, key=lambda x: x['total_quantity'], reverse=True)[:20],
        'total_products': Product.objects.count(),
        'total_quantity': Product.objects.aggregate(total=Sum('quantity'))['total'] or 0,
    }
    
    return render(request, 'admin/analytics/inventory_report.html', context)


@staff_member_required
def profit_report(request):
    """Profit and turnover analytics"""
    
    today = timezone.now().date()
    year = request.GET.get('year', today.year)
    
    # Yearly profit calculation
    yearly_profit = 0
    monthly_data = []
    
    for month in range(1, 13):
        # Get sales for month
        monthly_sales = SaleItem.objects.filter(
            sale__sale_date__year=year,
            sale__sale_date__month=month
        )
        
        # Calculate revenue
        monthly_revenue = sum(item.total_cost for item in monthly_sales)
        
        # Calculate COGS (Cost of Goods Sold)
        monthly_cogs = 0
        for sale_item in monthly_sales:
            # Find the cost price from arrivals
            arrival_item = ArrivalProduct.objects.filter(
                name=sale_item.product.name,
                article_number=sale_item.product.article_number
            ).first()
            
            if arrival_item:
                monthly_cogs += sale_item.quantity * arrival_item.cost_price
        
        monthly_profit = monthly_revenue - monthly_cogs
        
        monthly_data.append({
            'month': month,
            'revenue': monthly_revenue,
            'cogs': monthly_cogs,
            'profit': monthly_profit,
            'profit_margin': (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0
        })
        
        yearly_profit += monthly_profit
    
    # Annual turnover
    annual_turnover = Sale.objects.filter(
        sale_date__year=year
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Top profitable products
    profitable_products = []
    for product in Product.objects.all():
        # Get total sales
        sales_items = SaleItem.objects.filter(product=product)
        total_sold = sales_items.aggregate(total=Sum('quantity'))['total'] or 0
        
        if total_sold > 0:
            total_revenue = sum(item.total_cost for item in sales_items)
            
            # Find average cost price from arrivals
            arrival_items = ArrivalProduct.objects.filter(
                name=product.name,
                article_number=product.article_number
            )
            
            if arrival_items.exists():
                avg_cost = sum(item.cost_price for item in arrival_items) / arrival_items.count()
                total_profit = total_revenue - (total_sold * avg_cost)
                
                profitable_products.append({
                    'product': product,
                    'total_sold': total_sold,
                    'revenue': total_revenue,
                    'profit': total_profit,
                    'profit_margin': (total_profit / total_revenue * 100) if total_revenue > 0 else 0
                })
    
    profitable_products.sort(key=lambda x: x['profit'], reverse=True)
    
    context = {
        'title': 'Отчет по прибыли',
        'year': year,
        'monthly_data': monthly_data,
        'yearly_profit': yearly_profit,
        'annual_turnover': annual_turnover,
        'profitable_products': profitable_products[:20],
        'available_years': sorted(set(
            Sale.objects.dates('sale_date', 'year')
        ), reverse=True),
    }
    
    return render(request, 'admin/analytics/profit_report.html', context)