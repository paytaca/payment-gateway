from django.core.management.base import BaseCommand
from datetime import datetime
from django.db.models import Sum
from PaymentGateway.models import User, Order, TotalSalesByMonth

class Command(BaseCommand):
    help = 'Calculate and store total sales by month'

    def handle(self, *args, **options):
        # Get current year and month
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        # Get total sales by month for each user and store in TotalSalesByMonth model
        for user in User.objects.all():
            for month in range(1, current_month + 1):
                month_year_str = f'{current_year}-{month:02d}'
                total_sale = Order.objects.filter(
                    status = 'completed',
                    user = user,
                    created_at__year = current_year,
                    created_at__month = month
                    ).aggregate(Sum('total'))['total__sum'] or 0
                
                TotalSalesByMonth.objects.update_or_create(
                    user = user,
                    month = month_year_str,
                    defaults = {'total_sale': total_sale})

        self.stdout.write(self.style.SUCCESS('Successfully calculated and stored total sales by month.'))
        