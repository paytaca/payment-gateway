from django.core.management.base import BaseCommand
from woocommerce import API
from PaymentGateway.models import WoocommerceOrder, KeyAndSecret

class Command(BaseCommand):
    help = 'Get WooCommerce orders and store them in the database'

    def handle(self, *args, **options):
        for key_and_secret in KeyAndSecret.objects.all():
            wcapi = API(
                url=key_and_secret.store_url, #Store url
                consumer_key=key_and_secret.consumer_key, #consumer key from woocommerce setting
                consumer_secret=key_and_secret.consumer_secret, #consumer secret from woocommerce setting
                version="wc/v3",
                verify_ssl = False,
            )
            orders = wcapi.get("orders").json()
            for order in orders:
                WoocommerceOrder.objects.update_or_create(
                    order_id=order['id'],
                    username=key_and_secret.username,
                    defaults={
                        'customer_name': order['billing']['first_name'] + ' ' + order['billing']['last_name'],
                        'total': order['total'],
                        'status': order['status'],
                        'created_at': order['date_created'],
                        'updated_at': order["date_modified"],
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported WooCommerce orders.'))