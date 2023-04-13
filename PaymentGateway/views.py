import base64
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, Storefront

class ProcessOrderAPIView(APIView):
    def post(self, request):
        # Get the order ID from the request body
        order_id = request.data.get('order_id')

        # Get the order from the database
        order = get_object_or_404(Order, order_id=order_id)

        # Get the storefront associated with the order
        storefront = get_object_or_404(Storefront, user=order.user, store_url=order.store)

        # Update the status of the order
        order.status = 'completed'
        order.save()

        # Mark the order as completed in WooCommerce using the REST API
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
            return Response({'success': False})