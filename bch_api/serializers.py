from rest_framework import serializers
# from .models import Todo
from PaymentGateway.models import Account, Storefront, Order, TotalSales, TotalSalesYesterday, TotalSalesByMonth, TotalSalesByYear

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
        model = Account
        fields = ['user_id', 'email', 'username']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        
# ---------------------------------------------------------
# TOTAL SALES
# ---------------------------------------------------------
        
class TotalSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSales
        fields = '__all__'
    
class TotalSalesYesterdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSalesYesterday
        fields = '__all__'
        
class TotalSalesByMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSalesByMonth
        fields = '__all__'
        # fields = ["month", "total_sale"]
        
class TotalSalesByYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSalesByYear
        fields = '__all__'

# ---------------------------------------------------------
