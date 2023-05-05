from rest_framework import serializers
# from .models import Todo
from PaymentGateway.models import User, Storefront, Order, TotalSalesByMonth, TotalSales

class StorefrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storefront
        fields = '__all__'
        
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email']
        
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
