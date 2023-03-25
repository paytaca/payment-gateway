from django.core.management.base import BaseCommand
from woocommerce import API
from PaymentGateway.models import WoocommerceOrder

class Command(BaseCommand):
    help = 'Get WooCommerce orders and store them in the database'

    def handle(self, *args, **options):
        wcapi = API(
            url="https://paytaca-test.local",
            consumer_key="ck_8ec7450d792dba70c590869f3f551d988adcc7d1", #consumer key from woocommerce setting
            consumer_secret="cs_cec2598c50a006d10d1ce38e72305b50a3e6e64f", #consumer secret from woocommerce setting
            version="wc/v3",
            verify_ssl = False,
        )
        orders = wcapi.get("orders").json()
        for order in orders:
            WoocommerceOrder.objects.update_or_create(
                order_id=order['id'],
                defaults={
                    'customer_name': order['billing']['first_name'] + ' ' + order['billing']['last_name'],
                    'total': order['total'],
                    'status': order['status'],
                    'created_at': order['date_created'],
                    'updated_at': order["date_modified"],
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported WooCommerce orders.'))