from django.core.management.base import BaseCommand
from datetime import datetime
from django.db.models import Sum
from PaymentGateway.models import User, Order, TotalSalesByYear

class Command(BaseCommand):
    help = 'Calculate and store total sales by year'

    def handle(self, *args, **options):
        # Get current year
        now = datetime.now()
        current_year = now.year

        # Get total sales by year for each user and store in TotalSalesByYear model
        for user in User.objects.all():
            total_sale = Order.objects.filter(
                user = user,
                status = 'completed', 
                created_at__year = current_year
                ).aggregate(Sum('total'))['total__sum'] or 0
            
            TotalSalesByYear.objects.update_or_create(
                user = user,
                year = current_year,
                defaults = {'total_sale': total_sale})
            
        self.stdout.write(self.style.SUCCESS('Total sales by year calculated and stored successfully.'))
