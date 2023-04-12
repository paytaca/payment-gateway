from rest_framework import serializers
from .models import Todo
from PaymentGateway.models import Order, TotalSalesByMonth
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class TotalSalesByMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalSalesByMonth
        fields = '__all__'
