from django.core.management.base import BaseCommand
from django.db.models import Sum
from PaymentGateway.models import User, Order, TotalSales

class Command(BaseCommand):
    help = 'Calculate and store total sales for all users'

    def handle(self, *args, **options):
        # Get total sales for each user and store in TotalSales model
        for user in User.objects.all():
            total_sale = Order.objects.filter(
                user=user, 
                status='completed'
                ).aggregate(Sum('total'))['total__sum'] or 0
            
            TotalSales.objects.update_or_create(
                user=user,
                defaults={'total_sale': total_sale})
            
        self.stdout.write(self.style.SUCCESS('Total sales calculated and stored successfully.'))
