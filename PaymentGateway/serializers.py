from rest_framework import serializers

class GetOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    store_url = serializers.URLField()

class TotalBCHSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    store_url = serializers.URLField()

class ProcessOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    store_url = serializers.URLField()
    total_received = serializers.CharField()