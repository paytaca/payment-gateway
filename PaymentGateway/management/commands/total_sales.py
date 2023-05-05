from django.core.management.base import BaseCommand
from django.db.models import Sum
from PaymentGateway.models import Storefront, Order, TotalSales, TotalSalesYesterday, OrderItem
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Calculate and store today\'s total sales for all stores'

    def handle(self, *args, **options):
        # Get today's date and yesterday's date
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Get total sales for each storefront and store in TotalSales model for today's date
        for storefront in Storefront.objects.all():
            total_sale = Order.objects.filter(
                store=storefront,
                status='completed',
                created_at__date=today
            ).aggregate(Sum('total'))['total__sum'] or 0

            # Count the total orders for the storefront
            total_orders = Order.objects.filter(
                store=storefront,
                status='completed',
                created_at__date=today
            ).count()

            # Count the total of unique customers for the storefront
            total_customers = Order.objects.filter(
                store=storefront,
                status='completed',
                created_at__date=today
            ).values('customer_name').distinct().count()

            # Count the total products sold for the storefront
            products_sold = OrderItem.objects.filter(
                order__store=storefront,
                order__status='completed',
                order__created_at__date=today
            ).aggregate(products_sold=Sum('quantity'))['products_sold'] or 0

            yesterday_total_sales = TotalSalesYesterday.objects.filter(
                store=storefront,
                date_created=yesterday
            ).first()

            # Calculate the percentage changes from yesterday's values, if available
            if yesterday_total_sales:
                total_sale_percent = (yesterday_total_sales.total_sale - total_sale) / yesterday_total_sales.total_sale * 100
                total_orders_percent = (yesterday_total_sales.total_orders- total_orders) / yesterday_total_sales.total_orders / yesterday_total_sales.total_orders * 100
                total_customers_percent = (yesterday_total_sales.total_customers - total_customers) / yesterday_total_sales.total_customers * 100
                products_sold_percent = (yesterday_total_sales.products_sold - products_sold) / yesterday_total_sales.products_sold * 100

            # Update or create TotalSales object for the storefront and today's date
            TotalSales.objects.update_or_create(
                store=storefront,
                date_created=today,
                defaults={
                    'total_sale': total_sale,
                    'total_customers': total_customers,
                    'total_orders': total_orders,
                    'products_sold': products_sold,
                    'total_sale_percentage': total_sale_percent,
                    "total_orders_percentage": total_orders_percent,
                    'products_sold_percentage': products_sold_percent,
                    'total_customers_percentage': total_customers_percent
                })

        self.stdout.write(self.style.SUCCESS(f"Today's total sales calculated and stored successfully."))