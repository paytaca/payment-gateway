import base64
import requests
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from woocommerce import API
from django.shortcuts import get_object_or_404
from .models import Order, Storefront

class GetOrderAPIView(APIView):
    def post(self, request):
        # extract order details from the request
        order_id = request.data.get('order_id')
        store_url = request.data.get('store_url')

        # check if the store_url exists in Storefront model
        storefront = get_object_or_404(Storefront, store_url=store_url)

        # create the order only if the storefront exists using WooCommerceAPI
        wcapi = API(
            url=storefront.store_url,
            consumer_key=storefront.key,
            consumer_secret=storefront.secret,
            version="wc/v3",
            verify_ssl=False,
        )

        # get the order using the order_id and the WooCommerceAPI
        response = wcapi.get(f"orders/{order_id}")  
        if response.status_code != 200:
            return Response({'message': 'Invalid order ID'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = response.json()

        # get BCH exchange rate using CoinGecko API
        bch_rate = None
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "bitcoin-cash", "vs_currencies": order_data['currency'].lower()})
            response.raise_for_status()
            bch_rate = response.json()["bitcoin-cash"][order_data['currency'].lower()]
        except (requests.exceptions.RequestException, KeyError):
            pass

        # convert total to BCH
        total_bch = float(order_data['total'])
        if bch_rate is not None:
            total_bch /= bch_rate

        # save the order in the Order model
        order = Order(
            user=storefront.user,
            store=storefront.store_url,
            order_id=order_data['id'],
            customer_name=order_data['billing']['first_name'] + ' ' + order_data['billing']['last_name'],
            status=order_data['status'],
            total=order_data['total'],
            total_bch=total_bch,
            payment_method=order_data['payment_method'],
            created_at=order_data['date_created_gmt'],
            updated_at=order_data['date_modified_gmt']
        )
        order.save()

        return Response({'message': 'Order saved successfully'}, status=status.HTTP_201_CREATED)

class TotalBCHAPIView(APIView):
    def post(self, request):
        # get the order ID from the POST request
        order_id = request.data.get('order_id')
        store_url = request.data.get('store_url')

        # perform any necessary validation on the order ID
        if not order_id:
            return Response({'error': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # get the order object using the order ID
        order = get_object_or_404(Order, store=store_url, order_id=order_id)

        # calculate the total BCH based on the total amount of the order
        total_bch = order.total_bch

        # return the total BCH in a JSON response
        return Response({'total_bch': total_bch}, status=status.HTTP_200_OK)
        
class ProcessOrderAPIView(APIView):
    def post(self, request):
        # Get the order ID and store URL from the request body
        order_id = request.data.get('order_id')
        store_url = request.data.get('store_url')

        # Get the order from the database using the order ID and store URL
        order = get_object_or_404(Order, order_id=order_id, store=store_url)

        try:
            # Update the status of the order
            order.status = 'completed'
            order.updated_at = datetime.now()
            order.save()

            # Mark the order as completed in WooCommerce using the REST API
            # Get the storefront associated with the order
            storefront = get_object_or_404(Storefront, store_url=store_url)
            # Get the WooCommerce credentials from the storefront model
            wc_url = f'{storefront.store_url}/wp-json/wc/v3/orders/{order_id}'
            wc_key = storefront.key
            wc_secret = storefront.secret

            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f"{wc_key}:{wc_secret}".encode('utf-8')).decode('utf-8'),
                'Content-Type': 'application/json'
            }

            data = {
                'status': 'completed'
            }

            response = requests.put(wc_url, headers=headers, json=data, verify=False)

            # Return a JSON response indicating success or failure
            if response.ok:
                return Response({'success': True})
            else:
                return Response({'success': False, 'error': response.reason})

        except Exception as e:
            return Response({'success': False, 'error': str(e)})