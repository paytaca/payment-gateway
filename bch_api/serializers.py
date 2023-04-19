from rest_framework import serializers
# from .models import Todo
from PaymentGateway.models import User, Storefront, Order, TotalSalesByMonth, TotalSales, Test

class StorefrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storefront
        fields = '__all__'
        
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class TotalSalesByMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSalesByMonth
        fields = ["month", "total_sale"]

class TotalSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSales
        fields = '_all_'
        

''' kanan pagtesting han pasa pasa chuchu '''
        
# class TestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Test
#         fields = '__all__'
