from django.core.management.base import BaseCommand
from woocommerce import API
from PaymentGateway.models import Order, Storefront

class Command(BaseCommand):
    help = 'Get orders and store them in the database'

    def handle(self, *args, **options):
        for store in Storefront.objects.filter(store_type='woocommerce'):
            wcapi = API(
                url=store.store_url, #Store url
                consumer_key=store.key, #consumer key from woocommerce setting
                consumer_secret=store.secret, #consumer secret from woocommerce setting
                version="wc/v3",
                verify_ssl = False,
            )
            try:
                orders = wcapi.get("orders").json()
            except:
                self.stderr.write(self.style.ERROR(f'Error fetching orders for user {store.user}'))
                continue
            for order in orders:
                if order['payment_method'] == "bch_payment_gateway":
                    Order.objects.update_or_create(
                        order_id=order['id'],
                        store=store.store_type,
                        user=store.user,
                        defaults={
                            'customer_name': order['billing']['first_name'] + ' ' + order['billing']['last_name'],
                            'total': order['total'],
                            'status': order['status'],
                            'created_at': order['date_created'],
                            'updated_at': order["date_modified"],
                            'payment_method': order['payment_method'],
                        }
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported WooCommerce orders.'))