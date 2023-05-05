from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from PaymentGateway.models import TotalSalesYesterday, TotalSales, Storefront


class Command(BaseCommand):
    help = 'Move yesterday\'s total sales to TotalSalesYesterday and delete from TotalSales'

    def handle(self, *args, **options):
        yesterday = timezone.now() - timedelta(days=1)

        for storefront in Storefront.objects.all():
            yesterday_total_sales = TotalSales.objects.filter(
                store=storefront,
                date_created=yesterday
            ).first()

            if yesterday_total_sales:
                TotalSalesYesterday.objects.create(
                    store=storefront,
                    date_created=yesterday,
                    total_sale=yesterday_total_sales.total_sale,
                    total_customers=yesterday_total_sales.total_customers,
                    total_orders=yesterday_total_sales.total_orders,
                    products_sold=yesterday_total_sales.products_sold
                )

                yesterday_total_sales.delete()

        self.stdout.write(self.style.SUCCESS('Yesterday\'s total sales moved to TotalSalesYesterday and deleted from TotalSales.'))