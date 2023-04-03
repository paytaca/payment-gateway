from rest_framework import serializers
from .models import Todo
from PaymentGateway.models import Order
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["user", "order_id", "customer_name", "status", "total", "created_at", "updated_at"]
