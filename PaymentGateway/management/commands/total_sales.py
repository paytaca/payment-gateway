from django.core.management.base import BaseCommand
from django.db.models import Sum
from PaymentGateway.models import Storefront, Order, TotalSales

class Command(BaseCommand):
    help = 'Calculate and store total sales for all users'

    def handle(self, *args, **options):
        # Get total sales for each storefront and store in TotalSales model
        for storefront in Storefront.objects.all():
            total_sale = Order.objects.filter(
                store=storefront,
                status='completed'
            ).aggregate(Sum('total'))['total__sum'] or 0
            
            TotalSales.objects.update_or_create(
                store=storefront,
                defaults={'total_sale': total_sale})
            
        self.stdout.write(self.style.SUCCESS('Total sales calculated and stored successfully.'))
        