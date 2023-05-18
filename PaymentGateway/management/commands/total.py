from django.core.management.base import BaseCommand
from django.db.models import Sum
from PaymentGateway.models import Storefront, Order, Total

class Command(BaseCommand):
    help = 'Calculate and store all total sales'

    def handle(self, *args, **options):
        # Get total sales for each storefront and store in Total model
        for storefront in Storefront.objects.all():
                total_sale = Order.objects.filter(
                    status = 'completed',
                    store = storefront,
                ).aggregate(Sum('total')) or 0

                Total.objects.update_or_create(
                    store=storefront,
                    defaults={'total': total_sale})

        self.stdout.write(self.style.SUCCESS('Successfully calculated and stored total sales.'))