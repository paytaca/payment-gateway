from django.shortcuts import render
from django.http import JsonResponse
from .models import WoocommerceOrder
# Create your views here.

def order_list(request):
    orders = WoocommerceOrder.objects.all()
    data = [{
        'order_id': WoocommerceOrder.order_id,
        'customer_name': WoocommerceOrder.customer_name,
        'status': WoocommerceOrder.status,
        'total': WoocommerceOrder.total,
        'created_at': WoocommerceOrder.created_at,
        'updated_at': WoocommerceOrder.updated_at
    } for WoocommerceOrder in orders]

    return JsonResponse(data, safe = False)