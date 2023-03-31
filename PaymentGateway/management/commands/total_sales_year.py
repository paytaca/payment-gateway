from django.core.management.base import BaseCommand
from woocommerce import API
from PaymentGateway.models import Storefront, TotalSalesByYear
from datetime import datetime
from decimal import Decimal

class Command(BaseCommand):
    help = "Get total sales by year and store them in the database"

    def handle(self, *args, **options):
        for store in Storefront.objects.filter(store_type='woocommerce'):
            wcapi = API(
                url=store.store_url, #Store url
                consumer_key=store.key, #consumer key from woocommerce setting
                consumer_secret=store.secret, #consumer secret from woocommerce setting
                version="wc/v3",
                verify_ssl = False,
            )
            orders = wcapi.get("orders", params={"status": "completed"}).json()
            totals_by_year = {}
            for order in orders:
                year = datetime.strptime(order['date_created_gmt'], '%Y-%m-%dT%H:%M:%S').date().strftime('%Y')
                if year not in totals_by_year:
                    totals_by_year[year] = Decimal('0')
                totals_by_year[year] += Decimal(order['total'])

            for year, total_sale in totals_by_year.items():
                TotalSalesByYear.objects.update_or_create(
                    user=store.user,
                    year=year,
                    defaults={'total_sale': total_sale}
                )
                self.stdout.write(self.style.SUCCESS("Success Calculating Total Sales By Year"))